################################################################################
#
# Copyright (c) 2008, Kirk Reeves
# All rights reserved.
#
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# - Neither the name of the PYSDEE PROJECT nor the names of its contributors may
#   be used to endorse or promote products derived from this software without
#   specific prior written permission.
#
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
################################################################################


import urllib
import urllib2
import base64
import time
import types

import xml.dom.minidom


def parse_open(action, data):
    doc = xml.dom.minidom.parseString(data)
    header = doc.getElementsByTagName('env:Header')[0]
    oobinfo = header.getElementsByTagName('sd:oobInfo')[0]
    sess = oobinfo.getElementsByTagName('sd:sessionId')[0]
    sessionid = sess.firstChild.wholeText
    body = doc.getElementsByTagName('env:Body')[0]
    subscript = body.getElementsByTagName('sd:subscriptionId')[0]
    subscriptionid = subscript.firstChild.wholeText
    return [sessionid, subscriptionid]


def nano(epoch):
    return int(epoch * 1e9)


def epoch(nano):
    return (nano / 1e9)


class SDEE:

    def __init__(self, **kwargs):
        self._callback = kwargs.get('callback', '')
        self._format = kwargs.get('format', 'raw')
        self._timeout = kwargs.get('timeout', 1)
        self._user = kwargs.get('user', '')
        self._password = kwargs.get('password', '')
        self._host = kwargs.get('host', 'localhost')
        self._method = kwargs.get('method', 'https')
        self._resource = kwargs.get('resource', 'cgi-bin/sdee-server')
        self._uri = "%s://%s/%s" % (self._method, self._host, self._resource)
        self._sessionid = kwargs.get('sessionid', '')
        self._subscriptionid = kwargs.get('subscriptionid', '')
        self._starttime = kwargs.get('starttime', nano(time.time()))
        self._b64pass = base64.encodestring(
            "%s:%s" % (self._user, self._password))
        self._response = ''
        self._force = kwargs.get('force', 'no')
        self._established = False

    def data(self):
        return self._response

    def Password(self, passwd):
        self._password = passwd
        self._b64pass = base64.encodestring(
            "%s:%s" % (self._user, self._password))

    def User(self, username):
        self._user = username
        self._b64pass = base64.encodestring(
            "%s:%s" % (self._user, self._password))

    def Host(self, host):
        self._host = host
        self._uri = "%s://%s/%s" % (self._method, self._host, self._resource)

    def Method(self, method):
        self._method = method
        self._uri = "%s://%s/%s" % (self._method, self._host, self._resource)

    def Resource(self, resource):
        self._resource = resource
        self._uri = "%s://%s/%s" % (self._method, self._host, self._resource)

    def _request(self, params, **kwargs):
        req = urllib2.Request("%s?%s" % (self._uri, params))
        req.add_header('Authorization', "BASIC %s" % (self._b64pass))
        try:
            data = urllib2.urlopen(req)
            self._response = data.read()
        except:
            print "Connection Failed"

        if self._action == 'open':
            self._sessionid, self._subscriptionid = \
                parse_open(self._action, self._response)
            print ("Session ID: %s\t Subscription ID: %s" %
                   (self._sessionid, self._subscriptionid))
        elif self._action == 'close':
            print data.read()
        elif self._action == 'cancel':
            print data.read()
        elif self._action == 'get':
            if isinstance(self._callback, types.FunctionType):
                self._callback(**kwargs)
        elif self._action == 'query':
            pass

    def open(self, **kwargs):
        self._action = 'open'
        param_dict = {
            "events": "evIdsAlert",
            "action": "open",
            "force": self._force}
        if self._subscriptionid != '':
            param_dict['subscriptionId'] = self._subscriptionid
        params = urllib.urlencode(param_dict)
        self._request(params)

    def close(self, **kwargs):
        self._action = 'close'
        params = urllib.urlencode({
            "action": "close",
            "subscriptionId": self._subscriptionid})
        self._request(params)

    def cancel(self, **kwargs):
        self._action = 'cancel'
        params = urllib.urlencode({
            "action": "cancel",
            "subscriptionId": self._subscriptionid,
            "sessionId": self._sessionid})
        self._request(params)

    def get(self, **kwargs):
        self._action = 'get'
        params = urllib.urlencode({
            "confirm": "yes",
            "timeout": "1",
            "maxNbrofEvents": "20",
            "action": self._action,
            "subscriptionId": self._subscriptionid})
        self._request(params, **kwargs)

    def query(self, **kwargs):
        pass
