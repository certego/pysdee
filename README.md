
# pySDEE

**pySDEE is a library for accessing SDEE enabled security devices**
(specifically Cisco IDSM2 v5) which includes connecting to the IDSM and
decoding the XML response.

It has been developed by Kirk Reeves in 2008, and the original project website
is available on Google Code: https://code.google.com/p/pysdee/

Current release status is **incomplete/unfinished**.

## Installation

At the moment there is **no automated installation method**, so you need to
either copy the directory into site-packages, or embed all these files into
your project.

If you want an installer feel free to write it and open a pull request.

## Usage

Here are some examples taken from the original project website.

### Alerts to stdout

    from pysdee.pySDEE import SDEE
    from pysdee import idsmxml
    from time import sleep

    sdee = SDEE(user='username', password='password', host='192.168.1.1',
                method='https', force='yes')
    sdee.open()

    while True:
        sdee.get()
        alert_obj_list = idsmxml.parse_alerts(sdee.data())
        for alerts in alert_obj_list:
            print("alert_time: %s, severity: %s, signature: %s, " +
                "description: %s, attacker: %s, targets: %i" % (
                    alerts.alert_time, alerts.severity,
                    alerts.signature.id, alerts.signature.sigdetail,
                    alerts.attacker.addr, len(alerts.target_list)))
        sleep(5)

### Alerts to logfile

    from pysdee.pySDEE import SDEE
    from pysdee import idsmxml
    from pysdee.handler import logit
    from time import sleep

    sdee = SDEE(user='username', password='password', host='192.168.1.1',
                method='https', callback=logit, force='yes')
    sdee.open()

    file_handle = open('data.log', 'w+')
    while True:
        sdee.get(obj=sdee, file=file_handle)
        sleep(5)

    file_handle.close()

## License

Copyright (c) 2008, Kirk Reeves

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

 * Neither the name of the PYSDEE PROJECT nor the names of its contributors may
   be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

