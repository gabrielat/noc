# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# NAG.SNR.get_mac_address_table
# ---------------------------------------------------------------------
# Copyright (C) 2007-2012 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetmacaddresstable import IGetMACAddressTable


class Script(BaseScript):
    name = "NAG.SNR.get_mac_address_table"
    interface = IGetMACAddressTable
    cached = True

    def execute_snmp(self, interface=None, vlan=None, mac=None):
        r = []
        vlan_oid = []
        if mac is not None:
            mac = mac.lower()
        for v in self.snmp.get_tables(["1.3.6.1.2.1.17.7.1.2.2.1.2"], bulk=True):
            vlan_oid.append(v[0])
        # mac iface type
        for v in self.snmp.get_tables(
            ["1.3.6.1.2.1.17.4.3.1.1", "1.3.6.1.2.1.17.4.3.1.2", "1.3.6.1.2.1.17.4.3.1.3"],
            bulk=True,
        ):
            if v[1]:
                chassis = ":".join(["%02x" % ord(c) for c in v[1]])
                if mac is not None:
                    if chassis == mac:
                        pass
                    else:
                        continue
            else:
                continue
            if int(v[3]) > 3 or int(v[3]) < 1:
                continue
            iface = self.snmp.get("1.3.6.1.2.1.31.1.1.1.1." + str(v[2]), cached=True)  # IF-MIB
            if interface is not None:
                if iface == interface:
                    pass
                else:
                    continue
            for i in vlan_oid:
                if v[0] in i:
                    vlan_id = int(i.split(".")[0])
                    break
            if vlan is not None:
                if vlan_id == vlan:
                    pass
                else:
                    continue
            r += [
                {
                    "interfaces": [iface],
                    "mac": chassis,
                    "type": {"3": "D", "2": "S", "1": "S"}[str(v[3])],
                    "vlan_id": vlan_id,
                }
            ]
        return r
