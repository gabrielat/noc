# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS.get_copper_tdr_diag test
## Auto-generated by ./noc debug-script at 2011-12-14 16:58:12
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class DLink_DxS_get_copper_tdr_diag_Test(ScriptTestCase):
    script = "DLink.DxS.get_copper_tdr_diag"
    vendor = "DLink"
    platform = 'DES-3010G'
    version = '4.20.B27'
    input = {}
    result = [{'interface': '1',
  'pairs': [{'distance_cm': 77,
             'pair': 1,
             'status': 'O',
             'variance_cm': 100},
            {'distance_cm': 79,
             'pair': 2,
             'status': 'O',
             'variance_cm': 100},
            {'distance_cm': 0, 'pair': 3, 'status': 'N'},
            {'distance_cm': 0, 'pair': 4, 'status': 'N'}]},
 {'interface': '2',
  'pairs': [{'distance_cm': 300,
             'pair': 1,
             'status': 'T',
             'variance_cm': 100},
            {'distance_cm': 300,
             'pair': 2,
             'status': 'T',
             'variance_cm': 100},
            {'distance_cm': 300,
             'pair': 3,
             'status': 'T',
             'variance_cm': 100},
            {'distance_cm': 300,
             'pair': 4,
             'status': 'T',
             'variance_cm': 100}]},
 {'interface': '3',
  'pairs': [{'distance_cm': 9300,
             'pair': 1,
             'status': 'T',
             'variance_cm': 100},
            {'distance_cm': 9300,
             'pair': 2,
             'status': 'T',
             'variance_cm': 100},
            {'distance_cm': 9300,
             'pair': 3,
             'status': 'T',
             'variance_cm': 100},
            {'distance_cm': 9300,
             'pair': 4,
             'status': 'T',
             'variance_cm': 100}]},
 {'interface': '4',
  'pairs': [{'distance_cm': 0, 'pair': 1, 'status': 'N'},
            {'distance_cm': 0, 'pair': 2, 'status': 'N'},
            {'distance_cm': 0, 'pair': 3, 'status': 'N'},
            {'distance_cm': 0, 'pair': 4, 'status': 'N'}]},
 {'interface': '5',
  'pairs': [{'distance_cm': 0, 'pair': 1, 'status': 'N'},
            {'distance_cm': 0, 'pair': 2, 'status': 'N'},
            {'distance_cm': 0, 'pair': 3, 'status': 'N'},
            {'distance_cm': 0, 'pair': 4, 'status': 'N'}]},
 {'interface': '6',
  'pairs': [{'distance_cm': 0, 'pair': 1, 'status': 'N'},
            {'distance_cm': 0, 'pair': 2, 'status': 'N'},
            {'distance_cm': 0, 'pair': 3, 'status': 'N'},
            {'distance_cm': 0, 'pair': 4, 'status': 'N'}]},
 {'interface': '7',
  'pairs': [{'distance_cm': 0, 'pair': 1, 'status': 'N'},
            {'distance_cm': 0, 'pair': 2, 'status': 'N'},
            {'distance_cm': 0, 'pair': 3, 'status': 'N'},
            {'distance_cm': 0, 'pair': 4, 'status': 'N'}]},
 {'interface': '8',
  'pairs': [{'distance_cm': 0, 'pair': 1, 'status': 'N'},
            {'distance_cm': 0, 'pair': 2, 'status': 'N'},
            {'distance_cm': 0, 'pair': 3, 'status': 'N'},
            {'distance_cm': 0, 'pair': 4, 'status': 'N'}]}]
    motd = ''
    cli = {
## 'show switch'
'show switch': """show switch
Command: show switch

Device Type        : DES-3010G Fast Ethernet Switch
MAC Address        : 00-1B-11-B3-FC-CF
IP Address         : 10.116.0.11 (Manual)
VLAN Name          : upr
Subnet Mask        : 255.255.0.0
Default Gateway    : 10.116.0.1
Boot PROM Version  : Build 1.01.009
Firmware Version   : Build 4.20.B27
Hardware Version   : A3
System Name        : 
System Location    : Mira 31
System Contact     : 
Spanning Tree      : Disabled
LoopBack Detection : Enabled
IGMP Snooping      : Disabled
VLAN trunk         : Disabled
802.1X             : Disabled
TELNET             : Disabled
WEB                : Disabled
RMON               : Disabled
SSH                : Enabled(TCP  22)
Password Encryption: Enabled
""", 
## 'disable clipaging'
'disable clipaging': """disable clipaging
Command: disable clipaging

Success   
""", 
## 'cable_diag ports all'
'cable_diag ports all': """cable_diag ports all
Command: cable_diag ports all

 Perform Cable Diagnostics ...

 Port   Type      Link Status          Test Result          Cable Length (M)
 ----  -------  --------------  -------------------------  -----------------
  1      FE        Link Down     Pair1 Open      at 77  M          -
                                 Pair2 Open      at 79  M
                                 Pair3 Not Support
                                 Pair4 Not Support
  2      FE        Link Up       OK                                3
  3      FE        Link Up       OK                                93
  4      FE        Link Down     No Cable                          -
  5      FE        Link Down     No Cable                          -
  6      FE        Link Down     No Cable                          -
  7      FE        Link Down     No Cable                          -
  8      FE        Link Down     No Cable                          -
  9      GE        Link Down     Not Support                       -
  10    Fiber      Link Up       Not Support                       -
""", 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
