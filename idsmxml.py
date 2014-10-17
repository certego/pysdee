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


import xml.dom.minidom


class Participant:
    def __init__(self, **kwargs):
        self.xml = kwargs.get('xml', '')
        self.addr = kwargs.get('addr', '')
        self.port = kwargs.get('port', 0)


class Signature:
    def __init__(self, **kwargs):
        self.xml = kwargs.get('xml', '')
        self.id = kwargs.get('sigid', 0)
        self.version = kwargs.get('sigversion', '')
        self.subsig = kwargs.get('subsig', 0)
        self.sigdetail = kwargs.get('sigdetail', '')
        self.description = kwargs.get('sigdescription', '')


class Alert:
    def __init__(self, **kwargs):
        self.xml = kwargs.get('xml', '')
        self.eventid = kwargs.get('eventid', 0)
        self.severity = kwargs.get('severity', '')
        self.originator = kwargs.get('originator', '')
        self.alert_time = kwargs.get('alert_time', 0)
        self.signature = kwargs.get('signature', Signature())
        self.attacker = kwargs.get('attacker', Participant())
        self.target_list = kwargs.get('target_list', [])
        self.riskrating = kwargs.get('riskrating', 0)
        self.protocol = kwargs.get('protocol', '')


def build_global(node):

    alert = Alert()
    alert.xml = node.toxml()
    alert.eventid = node.attributes['eventId'].nodeValue
    alert.severity = node.attributes['severity'].nodeValue
    alert.originator = node.getElementsByTagName(
        'sd:originator')[0].getElementsByTagName(
        'sd:hostId')[0].firstChild.wholeText
    alert.alert_time = node.getElementsByTagName(
        'sd:time')[0].firstChild.wholeText
    alert.riskrating = node.getElementsByTagName(
        'cid:riskRatingValue')[0].firstChild.wholeText
    alert.protocol = node.getElementsByTagName(
        'cid:protocol')[0].firstChild.wholeText

    return alert


def build_sig(node):
    signature = Signature()
    signature.xml = node.toxml()
    signature.id = node.attributes['id'].nodeValue
    signature.version = node.attributes['cid:version'].nodeValue
    signature.description = node.attributes['description'].nodeValue
    signature.subsig = node.getElementsByTagName(
        'cid:subsigId')[0].firstChild.wholeText

    try:
        signature.sigdetail = node.getElementsByTagName(
            'cid:sigDetails')[0].firstChild.wholeText
    except:
        signature.sigdetail = node.attributes['description'].nodeValue

    return signature


def build_participant(node):

    targetnodelist = node.getElementsByTagName('sd:target')
    attacklist = node.getElementsByTagName('sd:attacker')
    if len(attacklist) == 1:
        attacker = Participant(xml=attacklist[0].toxml())
        attacker.addr = attacklist[0].getElementsByTagName(
            'sd:addr')[0].firstChild.wholeText
        try:
            attacker.port = attacklist[0].getElementsByTagName(
                'sd:port')[0].firstChild.wholeText
        except:
            attacker.port = '0'
    targetlist = []
    for item in targetnodelist:
        target = Participant(xml=item.toxml())
        target.addr = item.getElementsByTagName(
            'sd:addr')[0].firstChild.wholeText
        try:
            target.port = item.getElementsByTagName(
                'sd:port')[0].firstChild.wholeText
        except:
            target.port = '0'

        targetlist.append(target)

    return attacker, targetlist


def parse_alerts(xmldata):

    doc = xml.dom.minidom.parseString(xmldata)
    alertlist = doc.getElementsByTagName('sd:evIdsAlert')

    alert_obj_list = []
    for alert in alertlist:

        alert_obj = build_global(alert)

        sig = alert.getElementsByTagName('sd:signature')
        alert_obj.signature = build_sig(sig[0])

        participants = alert.getElementsByTagName('sd:participants')
        alert_obj.attacker, alert_obj.target_list = \
            build_participant(participants[0])

        alert_obj_list.append(alert_obj)

#    for alerts in alert_obj_list:
#        print "alert_time: %s, severity: %s, signature: %s, description: %s, attacker: %s, targets: %i" % (alerts.alert_time,
#                    alerts.severity, alerts.signature.id, alerts.signature.sigdetail, alerts.attacker.addr, len(alerts.target_list) )

    return alert_obj_list
