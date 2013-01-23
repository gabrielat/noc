# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## HP.ProCurve.get_spanning_tree test
## Auto-generated by ./noc debug-script at 21.01.2013 18:13:46
##----------------------------------------------------------------------
## Copyright (C) 2007-2013 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class HP_ProCurve_get_spanning_tree_Test(ScriptTestCase):
    script = "HP.ProCurve.get_spanning_tree"
    vendor = "HP"
    platform = "2520"
    version = "S.14.03"
    input = {}
    result = u'<type \'exceptions.KeyError\'>\nNone\nSTART OF TRACEBACK\n------------------------------------------------------------------------\nFile: /opt/noc/sa/profiles/HP/ProCurve/get_spanning_tree.py (Line: 49)\nFunction: mib_walk\n   42                         k = int(k)\n   43                     else:\n   44                         k = tuple([int(x) for x in k.split(".")])\n   45                     r[k] = v\n   46                     last_id = k\n   47                 else:\n   48                     # Multi-line value\n   49 ==>                 r[last_id] += "\\n" + l\n   50             return r\n   51     \n   52         ##\n   53         ## MSTP Parsing\n   54         ##\n   55         def process_mstp(self):\nVariables:\n                self = <Script(script-172.20.17.133-HP.ProCurve.get_spanning_tree, started 139635627267840)>\n                 oid = \'hpicfBridgeRstpOperEdgePort\'\n                   l = \'No such variable: hpicfBridgeRstpOperEdgePort.\'\n                   r = {}\n               l_oid = 28\n             last_id = None\n------------------------------------------------------------------------\nFile: /opt/noc/sa/profiles/HP/ProCurve/get_spanning_tree.py (Line: 254)\nFunction: process_rstp\n  247             v = self.mib_walk("dot1dBasePortIfIndex")\n  248             for port_id in v:\n  249                 ports[port_id] = {\n  250                     "interface": ifname[int(v[port_id])],\n  251                     "port_id": port_id,\n  252                 }\n  253             # Edge port status\n  254 ==>         v = self.mib_walk("hpicfBridgeRstpOperEdgePort")\n  255             for port_id in v:\n  256                 ports[port_id]["edge"] = v[port_id] == "1"\n  257             # point_to_point status\n  258             v = self.mib_walk("hpicfBridgeRstpOperPointToPointMac")\n  259             for port_id in v:\n  260                 ports[port_id]["point_to_point"] = v[port_id] == "1"\nVariables:\n           bridge_id = \'082e5f-e09b80\'\n                self = <Script(script-172.20.17.133-HP.ProCurve.get_spanning_tree, started 139635627267840)>\n                   l = \'\'\n            instance = {\'bridge_id\': \'082e5f-e09b80\', \'vlans\': \'1-4095\', \'id\': 0}\n                   r = {\'mode\': \'RSTP\'}\n                   v = {1: \'1\', 2: \'2\', 3: \'3\', 4: \'4\', 5: \'5\', 6: \'6\', 7: \'7\', 8: \'8\', 9: \'9\', 10: \'10\', 11: \'11\', 12: \'12\', 13: \'13\', 14: \'14\', 15: \'15\', 16: \'16\', 17: \'17\', 18: \'18\', 19: \'19\', 20: \'20\', 21: \'21\', 22: \'22\', 23: \'23\', 24: \'24\', 25: \'25\', 26: \'26\', 27: \'27\', 28: \'28\'}\n              ifname = {1: \'1\', 2: \'2\', 3: \'3\', 4: \'4\', 5: \'5\', 6: \'6\', 7: \'7\', 8: \'8\', 9: \'9\', 10: \'10\', 11: \'11\', 12: \'12\', 13: \'13\', 14: \'14\', 15: \'15\', 16: \'16\', 17: \'17\', 18: \'18\', 19: \'19\', 20: \'20\', 21: \'21\', 22: \'22\', 23: \'23\', 24: \'24\', 25: \'25\', 26: \'26\', 27: \'27\', 28: \'28\', 257: \'VLAN200\', 307: \'VLAN250\', 4152: \'lo0\', 4153: \'lo1\', 58: \'DEFAULT_VLAN\', 4155: \'lo3\', 4156: \'lo4\', 4157: \'lo5\', 4158: \'lo6\', 4159: \'lo7\', 67: \'VLAN10\', 77: \'VLAN20\', 87: \'VLAN30\', 4154: \'lo2\', 357: \'VLAN300\'}\n             port_id = 28\n               ports = {1: {\'interface\': \'1\', \'port_id\': 1}, 2: {\'interface\': \'2\', \'port_id\': 2}, 3: {\'interface\': \'3\', \'port_id\': 3}, 4: {\'interface\': \'4\', \'port_id\': 4}, 5: {\'interface\': \'5\', \'port_id\': 5}, 6: {\'interface\': \'6\', \'port_id\': 6}, 7: {\'interface\': \'7\', \'port_id\': 7}, 8: {\'interface\': \'8\', \'port_id\': 8}, 9: {\'interface\': \'9\', \'port_id\': 9}, 10: {\'interface\': \'10\', \'port_id\': 10}, 11: {\'interface\': \'11\', \'port_id\': 11}, 12: {\'interface\': \'12\', \'port_id\': 12}, 13: {\'interface\': \'13\', \'port_id\': 13}, 14: {\'interface\': \'14\', \'port_id\': 14}, 15: {\'interface\': \'15\', \'port_id\': 15}, 16: {\'interface\': \'16\', \'port_id\': 16}, 17: {\'interface\': \'17\', \'port_id\': 17}, 18: {\'interface\': \'18\', \'port_id\': 18}, 19: {\'interface\': \'19\', \'port_id\': 19}, 20: {\'interface\': \'20\', \'port_id\': 20}, 21: {\'interface\': \'21\', \'port_id\': 21}, 22: {\'interface\': \'22\', \'port_id\': 22}, 23: {\'interface\': \'23\', \'port_id\': 23}, 24: {\'interface\': \'24\', \'port_id\': 24}, 25: {\'interface\': \'25\', \'port_id\': 25}, 26: {\'interface\': \'26\', \'port_id\': 26}, 27: {\'interface\': \'27\', \'port_id\': 27}, 28: {\'interface\': \'28\', \'port_id\': 28}}\n------------------------------------------------------------------------\nFile: /opt/noc/sa/profiles/HP/ProCurve/get_spanning_tree.py (Line: 303)\nFunction: execute\n  296         def execute(self):\n  297             stp_version = self.mib_get("hpicfBridgeRstpForceVersion")\n  298             if stp_version == "1":\n  299                 # STP\n  300                 pass\n  301             elif stp_version == "2":\n  302                 # RSTP\n  303 ==>             return self.process_rstp()\n  304             elif stp_version == "3":\n  305                 # MSTP\n  306                 return self.process_mstp()\nVariables:\n                self = <Script(script-172.20.17.133-HP.ProCurve.get_spanning_tree, started 139635627267840)>\n         stp_version = \'2\'\n------------------------------------------------------------------------\nFile: /opt/noc/sa/script/script.py (Line: 417)\nFunction: guarded_run\n  410                     return result\n  411                 except KeyError:\n  412                     self.debug("Not in call cache: %r, %r" % (self.name,\n  413                                                               self.kwargs))\n  414                     pass\n  415                 # Calling script body\n  416             self._thread_id = thread.get_ident()\n  417 ==>         result = self.execute(**self.kwargs)\n  418             # Enforce interface result checking\n  419             for i in self.implements:\n  420                 result = i.script_clean_result(self.profile, result)\n  421             # Cache result when required\n  422             if self.cache and self.parent is not None:\n  423                 self.debug("Write to call cache: %s, %s, %r" % (self.name,\nVariables:\n                   i = <noc.sa.interfaces.igetspanningtree.IGetSpanningTree object at 0x335dd90>\n                self = <Script(script-172.20.17.133-HP.ProCurve.get_spanning_tree, started 139635627267840)>\n------------------------------------------------------------------------\nFile: /opt/noc/sa/script/script.py (Line: 440)\nFunction: run\n  433     \n  434         def run(self):\n  435             """Script thread worker method"""\n  436             self.debug("Running")\n  437             result = None\n  438             try:\n  439                 with self.cancelable():\n  440 ==>                 result = self.guarded_run()\n  441             except self.TimeOutError:\n  442                 self.error("Timed out")\n  443                 self.e_timeout = True\n  444             except CancelledError:\n  445                 self.error("Cancelled")\n  446                 self.e_cancel = True\nVariables:\n                self = <Script(script-172.20.17.133-HP.ProCurve.get_spanning_tree, started 139635627267840)>\n                   r = ["<type \'exceptions.KeyError\'>", \'None\']\n              result = None\n                   v = KeyError(None,)\n                  tb = <traceback object at 0x3fab758>\n                   t = <type \'exceptions.KeyError\'>\n------------------------------------------------------------------------\nEND OF TRACEBACK'
    motd = ''
    cli = {
'walkMIB hpicfBridgeRstpForceVersion':  'walkMIB hpicfBridgeRstpForceVersionhpicfBridgeRstpForceVersion.0 = 2\n', 
## 'walkMIB dot1dBasePortIfIndex'
'walkMIB dot1dBasePortIfIndex': """walkMIB dot1dBasePortIfIndexdot1dBasePortIfIndex.1 = 1
dot1dBasePortIfIndex.2 = 2
dot1dBasePortIfIndex.3 = 3
dot1dBasePortIfIndex.4 = 4
dot1dBasePortIfIndex.5 = 5
dot1dBasePortIfIndex.6 = 6
dot1dBasePortIfIndex.7 = 7
dot1dBasePortIfIndex.8 = 8
dot1dBasePortIfIndex.9 = 9
dot1dBasePortIfIndex.10 = 10
dot1dBasePortIfIndex.11 = 11
dot1dBasePortIfIndex.12 = 12
dot1dBasePortIfIndex.13 = 13
dot1dBasePortIfIndex.14 = 14
dot1dBasePortIfIndex.15 = 15
dot1dBasePortIfIndex.16 = 16
dot1dBasePortIfIndex.17 = 17
dot1dBasePortIfIndex.18 = 18
dot1dBasePortIfIndex.19 = 19
dot1dBasePortIfIndex.20 = 20
dot1dBasePortIfIndex.21 = 21
dot1dBasePortIfIndex.22 = 22
dot1dBasePortIfIndex.23 = 23
dot1dBasePortIfIndex.24 = 24
dot1dBasePortIfIndex.25 = 25
dot1dBasePortIfIndex.26 = 26
dot1dBasePortIfIndex.27 = 27
dot1dBasePortIfIndex.28 = 28""", 
'terminal length 1000':  'terminal length ', 
## 'sh spanning-tree instance ist'
'sh spanning-tree instance ist': """sh spanning-tree instance ist
 MST Instance Information

  STP Enabled   : No 
""", 
'walkMIB dot1dBaseBridgeAddress':  'walkMIB dot1dBaseBridgeAddressdot1dBaseBridgeAddress.0 = 08 2e 5f e0 9b 80 \n', 
## 'walkMIB ifName'
'walkMIB ifName': """walkMIB ifNameifName.1 = 1
ifName.2 = 2
ifName.3 = 3
ifName.4 = 4
ifName.5 = 5
ifName.6 = 6
ifName.7 = 7
ifName.8 = 8
ifName.9 = 9
ifName.10 = 10
ifName.11 = 11
ifName.12 = 12
ifName.13 = 13
ifName.14 = 14
ifName.15 = 15
ifName.16 = 16
ifName.17 = 17
ifName.18 = 18
ifName.19 = 19
ifName.20 = 20
ifName.21 = 21
ifName.22 = 22
ifName.23 = 23
ifName.24 = 24
ifName.25 = 25
ifName.26 = 26
ifName.27 = 27
ifName.28 = 28
ifName.58 = DEFAULT_VLAN
ifName.67 = VLAN10
ifName.77 = VLAN20
ifName.87 = VLAN30
ifName.257 = VLAN200
ifName.307 = VLAN250
ifName.357 = VLAN300
ifName.4152 = lo0
ifName.4153 = lo1
ifName.4154 = lo2
ifName.4155 = lo3
ifName.4156 = lo4
ifName.4157 = lo5
ifName.4158 = lo6
ifName.4159 = lo7""", 
'walkMIB hpicfBridgeRstpOperEdgePort':  'walkMIB hpicfBridgeRstpOperEdgePortNo such variable: hpicfBridgeRstpOperEdgePort.\n', 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
