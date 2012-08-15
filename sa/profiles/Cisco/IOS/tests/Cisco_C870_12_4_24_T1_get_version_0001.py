# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_version test
## Auto-generated by ./noc debug-script at 14.08.2012 13:38:11
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Cisco_IOS_get_version_Test(ScriptTestCase):
    script = "Cisco.IOS.get_version"
    vendor = "Cisco"
    platform = "C870"
    version = "12.4(24)T1"
    input = {}
    result = {'attributes': {'image': 'C870-ADVIPSERVICESK9-M'},
 'platform': 'C870',
 'vendor': 'Cisco',
 'version': '12.4(24)T1'}
    motd = ''
    cli = {
## 'show version'
'show version': """show version
Cisco IOS Software, C870 Software (C870-ADVIPSERVICESK9-M), Version 12.4(24)T1, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2009 by Cisco Systems, Inc.
Compiled Sat 20-Jun-09 02:20 by prod_rel_team

ROM: System Bootstrap, Version 12.3(8r)YI4, RELEASE SOFTWARE

sary uptime is 8 weeks, 3 days, 3 hours, 2 minutes
System returned to ROM by power-on
System restarted at 10:55:28 Moscow Sat Jun 16 2012
System image file is "flash:c870-advipservicesk9-mz.124-24.T1.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

Cisco 871 (MPC8272) processor (revision 0x300) with 118784K/12288K bytes of memory.
Processor board ID FCZ122492RM
MPC8272 CPU Rev: Part Number 0xC, Mask Number 0x10
5 FastEthernet interfaces
128K bytes of non-volatile configuration memory.
24576K bytes of processor board System flash (Intel Strataflash)

Configuration register is 0x2102
""", 
'terminal length 0':  'terminal length 0\n', 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
