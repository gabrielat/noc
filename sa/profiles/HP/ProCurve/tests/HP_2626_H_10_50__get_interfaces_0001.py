# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## HP.ProCurve.get_interfaces test
## Auto-generated by ./noc debug-script at 21.01.2013 18:07:51
##----------------------------------------------------------------------
## Copyright (C) 2007-2013 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class HP_ProCurve_get_interfaces_Test(ScriptTestCase):
    script = "HP.ProCurve.get_interfaces"
    vendor = "HP"
    platform = "2626"
    version = "H.10.50 "
    input = {}
    result = [{'forwarding_instance': 'default',
  'interfaces': [{'admin_status': True,
                  'description': '1',
                  'mac': '00:1C:2E:3A:60:BF',
                  'name': '1',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '1',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:BF',
                                     'name': '1',
                                     'oper_status': True,
                                     'snmp_ifindex': 1,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '2',
                  'mac': '00:1C:2E:3A:60:BE',
                  'name': '2',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '2',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:BE',
                                     'name': '2',
                                     'oper_status': True,
                                     'snmp_ifindex': 2,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '3',
                  'mac': '00:1C:2E:3A:60:BD',
                  'name': '3',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '3',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:BD',
                                     'name': '3',
                                     'oper_status': True,
                                     'snmp_ifindex': 3,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '4',
                  'mac': '00:1C:2E:3A:60:BC',
                  'name': '4',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '4',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:BC',
                                     'name': '4',
                                     'oper_status': True,
                                     'snmp_ifindex': 4,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '5',
                  'mac': '00:1C:2E:3A:60:BB',
                  'name': '5',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '5',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:BB',
                                     'name': '5',
                                     'oper_status': False,
                                     'snmp_ifindex': 5,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '6',
                  'mac': '00:1C:2E:3A:60:BA',
                  'name': '6',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '6',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:BA',
                                     'name': '6',
                                     'oper_status': False,
                                     'snmp_ifindex': 6,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '7',
                  'mac': '00:1C:2E:3A:60:B9',
                  'name': '7',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '7',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:B9',
                                     'name': '7',
                                     'oper_status': True,
                                     'snmp_ifindex': 7,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '8',
                  'mac': '00:1C:2E:3A:60:B8',
                  'name': '8',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '8',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:B8',
                                     'name': '8',
                                     'oper_status': True,
                                     'snmp_ifindex': 8,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '9',
                  'mac': '00:1C:2E:3A:60:B7',
                  'name': '9',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '9',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:B7',
                                     'name': '9',
                                     'oper_status': True,
                                     'snmp_ifindex': 9,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '10',
                  'mac': '00:1C:2E:3A:60:B6',
                  'name': '10',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '10',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:B6',
                                     'name': '10',
                                     'oper_status': True,
                                     'snmp_ifindex': 10,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '11',
                  'mac': '00:1C:2E:3A:60:B5',
                  'name': '11',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '11',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:B5',
                                     'name': '11',
                                     'oper_status': True,
                                     'snmp_ifindex': 11,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '12',
                  'mac': '00:1C:2E:3A:60:B4',
                  'name': '12',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '12',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:B4',
                                     'name': '12',
                                     'oper_status': True,
                                     'snmp_ifindex': 12,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '13',
                  'mac': '00:1C:2E:3A:60:B3',
                  'name': '13',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '13',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:B3',
                                     'name': '13',
                                     'oper_status': True,
                                     'snmp_ifindex': 13,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '14',
                  'mac': '00:1C:2E:3A:60:B2',
                  'name': '14',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '14',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:B2',
                                     'name': '14',
                                     'oper_status': True,
                                     'snmp_ifindex': 14,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '15',
                  'mac': '00:1C:2E:3A:60:B1',
                  'name': '15',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '15',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:B1',
                                     'name': '15',
                                     'oper_status': True,
                                     'snmp_ifindex': 15,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '16',
                  'mac': '00:1C:2E:3A:60:B0',
                  'name': '16',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '16',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:B0',
                                     'name': '16',
                                     'oper_status': True,
                                     'snmp_ifindex': 16,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '17',
                  'mac': '00:1C:2E:3A:60:AF',
                  'name': '17',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '17',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:AF',
                                     'name': '17',
                                     'oper_status': False,
                                     'snmp_ifindex': 17,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '18',
                  'mac': '00:1C:2E:3A:60:AE',
                  'name': '18',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '18',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:AE',
                                     'name': '18',
                                     'oper_status': True,
                                     'snmp_ifindex': 18,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '19',
                  'mac': '00:1C:2E:3A:60:AD',
                  'name': '19',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '19',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:AD',
                                     'name': '19',
                                     'oper_status': True,
                                     'snmp_ifindex': 19,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '20',
                  'mac': '00:1C:2E:3A:60:AC',
                  'name': '20',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '20',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:AC',
                                     'name': '20',
                                     'oper_status': False,
                                     'snmp_ifindex': 20,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '21',
                  'mac': '00:1C:2E:3A:60:AB',
                  'name': '21',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '21',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:AB',
                                     'name': '21',
                                     'oper_status': True,
                                     'snmp_ifindex': 21,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '22',
                  'mac': '00:1C:2E:3A:60:AA',
                  'name': '22',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '22',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:AA',
                                     'name': '22',
                                     'oper_status': True,
                                     'snmp_ifindex': 22,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '23',
                  'mac': '00:1C:2E:3A:60:A9',
                  'name': '23',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '23',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:A9',
                                     'name': '23',
                                     'oper_status': True,
                                     'snmp_ifindex': 23,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '24',
                  'mac': '00:1C:2E:3A:60:A8',
                  'name': '24',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '24',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:A8',
                                     'name': '24',
                                     'oper_status': True,
                                     'snmp_ifindex': 24,
                                     'tagged_vlans': [16],
                                     'untagged_vlan': 20}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '25',
                  'mac': '00:1C:2E:3A:60:A7',
                  'name': '25',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '25',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:A7',
                                     'name': '25',
                                     'oper_status': True,
                                     'snmp_ifindex': 25,
                                     'tagged_vlans': [16, 2],
                                     'untagged_vlan': 1}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': '26',
                  'mac': '00:1C:2E:3A:60:A6',
                  'name': '26',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': '26',
                                     'is_bridge': True,
                                     'mac': '00:1C:2E:3A:60:A6',
                                     'name': '26',
                                     'oper_status': True,
                                     'snmp_ifindex': 26,
                                     'tagged_vlans': [16, 2],
                                     'untagged_vlan': 1}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': 'DEFAULT_VLAN',
                  'mac': '00:1C:2E:3A:60:80',
                  'name': 'DEFAULT_VLAN',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': 'DEFAULT_VLAN',
                                     'mac': '00:1C:2E:3A:60:80',
                                     'name': 'DEFAULT_VLAN',
                                     'oper_status': True,
                                     'snmp_ifindex': 63}],
                  'type': 'SVI'},
                 {'admin_status': True,
                  'description': 'Management',
                  'mac': '00:1C:2E:3A:60:80',
                  'name': 'Management',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': 'Management',
                                     'ipv4_addresses': ['192.168.2.22/24'],
                                     'is_ipv4': True,
                                     'mac': '00:1C:2E:3A:60:80',
                                     'name': 'Management',
                                     'oper_status': True,
                                     'snmp_ifindex': 64}],
                  'type': 'SVI'},
                 {'admin_status': True,
                  'description': 'IPTel',
                  'mac': '00:1C:2E:3A:60:80',
                  'name': 'IPTel',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': 'IPTel',
                                     'mac': '00:1C:2E:3A:60:80',
                                     'name': 'IPTel',
                                     'oper_status': True,
                                     'snmp_ifindex': 78}],
                  'type': 'SVI'},
                 {'admin_status': True,
                  'description': 'Users',
                  'mac': '00:1C:2E:3A:60:80',
                  'name': 'Users',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': 'Users',
                                     'mac': '00:1C:2E:3A:60:80',
                                     'name': 'Users',
                                     'oper_status': True,
                                     'snmp_ifindex': 82}],
                  'type': 'SVI'},
                 {'admin_status': True,
                  'description': 'HP ProCurve Switch software loopback interface',
                  'name': 'lo0',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'description': 'HP ProCurve Switch software loopback interface',
                                     'name': 'lo0',
                                     'oper_status': True,
                                     'snmp_ifindex': 4158}],
                  'type': 'loopback'}],
  'type': 'ip'}]
    motd = ''
    cli = {
## 'show ip'
'show ip': """show ip
 Internet (IP) Service

  IP Routing : Disabled

  Default Gateway :                
  Default TTL     : 64   
  Arp Age         : 20  

  VLAN         | IP Config  IP Address      Subnet Mask    
  ------------ + ---------- --------------- ---------------
  DEFAULT_VLAN | Disabled  
  Management   | Manual     192.168.2.22    255.255.255.0   
  IPTel        | Disabled  
  Users        | Disabled  
 
""", 
## 'show trunks'
'show trunks': """show trunks
 Load Balancing

  Port | Name                             Type      | Group Type 
  ---- + -------------------------------- --------- + ----- -----
 
""", 
'show ip ospf interface':  'show ip ospf interfaceInvalid input: ospf\n', 
'terminal length 1000':  'terminal length ', 
## 'walkMIB ifName ifOperStatus ifDescr'
'walkMIB ifName ifOperStatus ifDescr': """walkMIB ifName ifOperStatus ifDescrifName.1 = 1
ifOperStatus.1 = 1
ifDescr.1 = 1
ifName.2 = 2
ifOperStatus.2 = 1
ifDescr.2 = 2
ifName.3 = 3
ifOperStatus.3 = 1
ifDescr.3 = 3
ifName.4 = 4
ifOperStatus.4 = 1
ifDescr.4 = 4
ifName.5 = 5
ifOperStatus.5 = 2
ifDescr.5 = 5
ifName.6 = 6
ifOperStatus.6 = 2
ifDescr.6 = 6
ifName.7 = 7
ifOperStatus.7 = 1
ifDescr.7 = 7
ifName.8 = 8
ifOperStatus.8 = 1
ifDescr.8 = 8
ifName.9 = 9
ifOperStatus.9 = 1
ifDescr.9 = 9
ifName.10 = 10
ifOperStatus.10 = 1
ifDescr.10 = 10
ifName.11 = 11
ifOperStatus.11 = 1
ifDescr.11 = 11
ifName.12 = 12
ifOperStatus.12 = 1
ifDescr.12 = 12
ifName.13 = 13
ifOperStatus.13 = 1
ifDescr.13 = 13
ifName.14 = 14
ifOperStatus.14 = 1
ifDescr.14 = 14
ifName.15 = 15
ifOperStatus.15 = 1
ifDescr.15 = 15
ifName.16 = 16
ifOperStatus.16 = 1
ifDescr.16 = 16
ifName.17 = 17
ifOperStatus.17 = 2
ifDescr.17 = 17
ifName.18 = 18
ifOperStatus.18 = 1
ifDescr.18 = 18
ifName.19 = 19
ifOperStatus.19 = 1
ifDescr.19 = 19
ifName.20 = 20
ifOperStatus.20 = 2
ifDescr.20 = 20
ifName.21 = 21
ifOperStatus.21 = 1
ifDescr.21 = 21
ifName.22 = 22
ifOperStatus.22 = 1
ifDescr.22 = 22
ifName.23 = 23
ifOperStatus.23 = 1
ifDescr.23 = 23
ifName.24 = 24
ifOperStatus.24 = 1
ifDescr.24 = 24
ifName.25 = 25
ifOperStatus.25 = 1
ifDescr.25 = 25
ifName.26 = 26
ifOperStatus.26 = 1
ifDescr.26 = 26
ifName.63 = DEFAULT_VLAN
ifOperStatus.63 = 1
ifDescr.63 = DEFAULT_VLAN
ifName.64 = Management
ifOperStatus.64 = 1
ifDescr.64 = Management
ifName.78 = IPTel
ifOperStatus.78 = 1
ifDescr.78 = IPTel
ifName.82 = Users
ifOperStatus.82 = 1
ifDescr.82 = Users
ifName.4158 = lo0
ifOperStatus.4158 = 1
ifDescr.4158 = HP ProCurve Switch software loopback interface""", 
## 'walkMIB dot1qVlanStaticUntaggedPorts dot1qVlanStaticEgressPorts'
'walkMIB dot1qVlanStaticUntaggedPorts dot1qVlanStaticEgressPorts': """walkMIB dot1qVlanStaticUntaggedPorts dot1qVlanStaticEgressPortsdot1qVlanStaticUntaggedPorts.1 = 00 00  00 ff   ff ff  ff fc    
dot1qVlanStaticEgressPorts.1 = 00 00  00 ff   ff ff  ff fc    
dot1qVlanStaticUntaggedPorts.2 = 00 00  00 00   00 00  00 00    
dot1qVlanStaticEgressPorts.2 = 00 00  00 c0   00 00  00 00    
dot1qVlanStaticUntaggedPorts.16 = 00 00  00 00   00 00  00 00    
dot1qVlanStaticEgressPorts.16 = ff ff  ff c0   00 00  00 00    
dot1qVlanStaticUntaggedPorts.20 = ff ff  ff 00   00 00  00 00    
dot1qVlanStaticEgressPorts.20 = ff ff  ff c0   00 00  00 00    """, 
## 'show vlans'
'show vlans': """show vlans
 Status and Counters - VLAN Information

  Maximum VLANs to support : 253                  
  Primary VLAN : DEFAULT_VLAN
  Management VLAN :             

  802.1Q VLAN ID Name         Status       Voice
  -------------- ------------ ------------ -----
  1              DEFAULT_VLAN Port-based   No   
  2              Management   Port-based   No   
  16             IPTel        Port-based   No   
  20             Users        Port-based   No   
 
""", 
'walkMIB dot1dBaseNumPorts':  'walkMIB dot1dBaseNumPortsdot1dBaseNumPorts.0 = 26\n', 
## 'walkMIB ifType ifPhysAddress ifAdminStatus ifDescr ifName ifOperStatus'
'walkMIB ifType ifPhysAddress ifAdminStatus ifDescr ifName ifOperStatus': """walkMIB ifType ifPhysAddress ifAdminStatus ifDescr ifName ifOperStatusifType.1 = 6
ifPhysAddress.1 = 00 1c 2e 3a 60 bf 
ifAdminStatus.1 = 1
ifDescr.1 = 1
ifName.1 = 1
ifOperStatus.1 = 1
ifType.2 = 6
ifPhysAddress.2 = 00 1c 2e 3a 60 be 
ifAdminStatus.2 = 1
ifDescr.2 = 2
ifName.2 = 2
ifOperStatus.2 = 1
ifType.3 = 6
ifPhysAddress.3 = 00 1c 2e 3a 60 bd 
ifAdminStatus.3 = 1
ifDescr.3 = 3
ifName.3 = 3
ifOperStatus.3 = 1
ifType.4 = 6
ifPhysAddress.4 = 00 1c 2e 3a 60 bc 
ifAdminStatus.4 = 1
ifDescr.4 = 4
ifName.4 = 4
ifOperStatus.4 = 1
ifType.5 = 6
ifPhysAddress.5 = 00 1c 2e 3a 60 bb 
ifAdminStatus.5 = 1
ifDescr.5 = 5
ifName.5 = 5
ifOperStatus.5 = 2
ifType.6 = 6
ifPhysAddress.6 = 00 1c 2e 3a 60 ba 
ifAdminStatus.6 = 1
ifDescr.6 = 6
ifName.6 = 6
ifOperStatus.6 = 2
ifType.7 = 6
ifPhysAddress.7 = 00 1c 2e 3a 60 b9 
ifAdminStatus.7 = 1
ifDescr.7 = 7
ifName.7 = 7
ifOperStatus.7 = 1
ifType.8 = 6
ifPhysAddress.8 = 00 1c 2e 3a 60 b8 
ifAdminStatus.8 = 1
ifDescr.8 = 8
ifName.8 = 8
ifOperStatus.8 = 1
ifType.9 = 6
ifPhysAddress.9 = 00 1c 2e 3a 60 b7 
ifAdminStatus.9 = 1
ifDescr.9 = 9
ifName.9 = 9
ifOperStatus.9 = 1
ifType.10 = 6
ifPhysAddress.10 = 00 1c 2e 3a 60 b6 
ifAdminStatus.10 = 1
ifDescr.10 = 10
ifName.10 = 10
ifOperStatus.10 = 1
ifType.11 = 6
ifPhysAddress.11 = 00 1c 2e 3a 60 b5 
ifAdminStatus.11 = 1
ifDescr.11 = 11
ifName.11 = 11
ifOperStatus.11 = 1
ifType.12 = 6
ifPhysAddress.12 = 00 1c 2e 3a 60 b4 
ifAdminStatus.12 = 1
ifDescr.12 = 12
ifName.12 = 12
ifOperStatus.12 = 1
ifType.13 = 6
ifPhysAddress.13 = 00 1c 2e 3a 60 b3 
ifAdminStatus.13 = 1
ifDescr.13 = 13
ifName.13 = 13
ifOperStatus.13 = 1
ifType.14 = 6
ifPhysAddress.14 = 00 1c 2e 3a 60 b2 
ifAdminStatus.14 = 1
ifDescr.14 = 14
ifName.14 = 14
ifOperStatus.14 = 1
ifType.15 = 6
ifPhysAddress.15 = 00 1c 2e 3a 60 b1 
ifAdminStatus.15 = 1
ifDescr.15 = 15
ifName.15 = 15
ifOperStatus.15 = 1
ifType.16 = 6
ifPhysAddress.16 = 00 1c 2e 3a 60 b0 
ifAdminStatus.16 = 1
ifDescr.16 = 16
ifName.16 = 16
ifOperStatus.16 = 1
ifType.17 = 6
ifPhysAddress.17 = 00 1c 2e 3a 60 af 
ifAdminStatus.17 = 1
ifDescr.17 = 17
ifName.17 = 17
ifOperStatus.17 = 2
ifType.18 = 6
ifPhysAddress.18 = 00 1c 2e 3a 60 ae 
ifAdminStatus.18 = 1
ifDescr.18 = 18
ifName.18 = 18
ifOperStatus.18 = 1
ifType.19 = 6
ifPhysAddress.19 = 00 1c 2e 3a 60 ad 
ifAdminStatus.19 = 1
ifDescr.19 = 19
ifName.19 = 19
ifOperStatus.19 = 1
ifType.20 = 6
ifPhysAddress.20 = 00 1c 2e 3a 60 ac 
ifAdminStatus.20 = 1
ifDescr.20 = 20
ifName.20 = 20
ifOperStatus.20 = 2
ifType.21 = 6
ifPhysAddress.21 = 00 1c 2e 3a 60 ab 
ifAdminStatus.21 = 1
ifDescr.21 = 21
ifName.21 = 21
ifOperStatus.21 = 1
ifType.22 = 6
ifPhysAddress.22 = 00 1c 2e 3a 60 aa 
ifAdminStatus.22 = 1
ifDescr.22 = 22
ifName.22 = 22
ifOperStatus.22 = 1
ifType.23 = 6
ifPhysAddress.23 = 00 1c 2e 3a 60 a9 
ifAdminStatus.23 = 1
ifDescr.23 = 23
ifName.23 = 23
ifOperStatus.23 = 1
ifType.24 = 6
ifPhysAddress.24 = 00 1c 2e 3a 60 a8 
ifAdminStatus.24 = 1
ifDescr.24 = 24
ifName.24 = 24
ifOperStatus.24 = 1
ifType.25 = 6
ifPhysAddress.25 = 00 1c 2e 3a 60 a7 
ifAdminStatus.25 = 1
ifDescr.25 = 25
ifName.25 = 25
ifOperStatus.25 = 1
ifType.26 = 6
ifPhysAddress.26 = 00 1c 2e 3a 60 a6 
ifAdminStatus.26 = 1
ifDescr.26 = 26
ifName.26 = 26
ifOperStatus.26 = 1
ifType.63 = 53
ifPhysAddress.63 = 00 1c 2e 3a 60 80 
ifAdminStatus.63 = 1
ifDescr.63 = DEFAULT_VLAN
ifName.63 = DEFAULT_VLAN
ifOperStatus.63 = 1
ifType.64 = 53
ifPhysAddress.64 = 00 1c 2e 3a 60 80 
ifAdminStatus.64 = 1
ifDescr.64 = Management
ifName.64 = Management
ifOperStatus.64 = 1
ifType.78 = 53
ifPhysAddress.78 = 00 1c 2e 3a 60 80 
ifAdminStatus.78 = 1
ifDescr.78 = IPTel
ifName.78 = IPTel
ifOperStatus.78 = 1
ifType.82 = 53
ifPhysAddress.82 = 00 1c 2e 3a 60 80 
ifAdminStatus.82 = 1
ifDescr.82 = Users
ifName.82 = Users
ifOperStatus.82 = 1
ifType.4158 = 24
ifPhysAddress.4158 = 
ifAdminStatus.4158 = 1
ifDescr.4158 = HP ProCurve Switch software loopback interface
ifName.4158 = lo0
ifOperStatus.4158 = 1""", 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
