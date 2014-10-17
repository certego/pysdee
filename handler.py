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


from pysdee import idsmxml


def log_to_file(file_handle, obj):
    global_str = "%s\t%s\t%s\t%s\t%s\t%s" % (
        obj.eventid,
        obj.severity,
        obj.originator,
        obj.alert_time,
        obj.riskrating,
        obj.protocol)
    sig_str = "%s\t%s\t%s\t%s" % (
        obj.signature.id,
        obj.signature.version,
        obj.signature.subsig,
        obj.signature.sigdetail)
    attacker_str = "%s\t%s" % (
        obj.attacker.addr,
        obj.attacker.port)

    for target in obj.target_list:
        target_str = "%s\t%s" % (
            target.addr,
            target.port)
        file_handle.write("%s\t%s\t%s\t%s\n" % (
            global_str,
            sig_str,
            attacker_str,
            target_str))


def display_events(**kwargs):
    obj = kwargs['obj']
    alert_obj_list = idsmxml.parse_alerts(obj._response)
    file = open('data.log', 'w+')
    for alerts in alert_obj_list:
        print "alert_time: %s, severity: %s, signature: %s, " \
            "description: %s, attacker: %s, targets: %i" % (
                alerts.alert_time,
                alerts.severity,
                alerts.signature.id,
                alerts.signature.sigdetail,
                alerts.attacker.addr,
                len(alerts.target_list))
        log_to_file(file, alerts)
        file.flush()
    file.close()


def display_high(**kwargs):
    obj = kwargs['obj']
    alert_obj_list = idsmxml.parse_alerts(obj._response)
    for alerts in alert_obj_list:
        if alerts.severity == 'high':
            print "alert_time: %s, severity: %s, signature: %s, " \
                "description: %s, attacker: %s, targets: %i" % (
                    alerts.alert_time,
                    alerts.severity,
                    alerts.signature.id,
                    alerts.signature.sigdetail,
                    alerts.attacker.addr,
                    len(alerts.target_list))


def logit(**kwargs):
    obj = kwargs['obj']
    file = kwargs['file']
    alert_obj_list = idsmxml.parse_alerts(obj._response)
    xmlout = open('outdata.xml', 'a+')
    for alerts in alert_obj_list:
        log_to_file(file, alerts)
        xmlout.write("%s\n" % alerts.xml)
    xmlout.close()
