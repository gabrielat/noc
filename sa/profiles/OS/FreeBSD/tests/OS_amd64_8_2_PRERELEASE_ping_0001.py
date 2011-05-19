# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## OS.FreeBSD.ping test
## Auto-generated by manage.py debug-script at 2011-04-26 09:24:15
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class OS_FreeBSD_ping_Test(ScriptTestCase):
    script="OS.FreeBSD.ping"
    vendor="OS"
    platform='amd64'
    version='8.2-PRERELEASE'
    input={'address': '10.111.0.1'}
    result={'avg': '0.164', 'count': 5, 'max': '0.241', 'min': '0.126', 'success': 5}
    motd='\n'
    cli={
## 'ping -q -c 5 10.111.0.1'
'ping -q -c 5 10.111.0.1': """ ping -q -c 5 10.111.0.1
PING 10.111.0.1 (10.111.0.1): 56 data bytes

--- 10.111.0.1 ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 0.126/0.164/0.241/0.041 ms""", 
}
    snmp_get={}
    snmp_getnext={}
