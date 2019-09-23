# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Raisecom.ROS.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
from collections import defaultdict

# Third-party modules
import six

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces
from noc.core.text import ranges_to_list
from noc.core.ip import IPv4


class Script(BaseScript):
    name = "Raisecom.ROS.get_interfaces"
    cache = True
    interface = IGetInterfaces

    rx_vlans = re.compile(
        r"^\s*(?:Interface: |: |Port: )?(?P<name>\d+|gigaethernet1/1/\d+)\s*\n"
        r"(^\s*Switch Mode: switch\n)?"
        r"(^\s*Reject frame type: \S+\n)?"
        r"^\s*Administrative\sMode:\s*(?P<adm_mode>.*)\n"
        r"^\s*Operational\sMode:\s*(?P<op_mode>.*)\n"
        r"^\s*Access\sMode\sVLAN:\s*(?P<untagged_vlan>.*)\n"
        r"^\s*Administrative\sAccess\sEgress\sVLANs:\s*(?P<mvr_vlan>.*)\n"
        r"^\s*Operational\sAccess\sEgress\sVLANs:\s*(?P<op_eg_vlan>.*)\n"
        r"^\s*Trunk(?:\sNative)?\sMode(?:\sNative)?\sVLAN:\s*(?P<trunk_native_vlan>.*)\n"
        r"(^\s*Trunk\sNative\sVLAN(?:\sStatus)?:\s*(?P<trunk_native_vlan_mode>.*)\n)?"
        r"^\s*Administrative\sTrunk\sAllowed\sVLANs:\s*(?P<adm_trunk_allowed_vlan>.*)\n"
        r"^\s*Operational\sTrunk\sAllowed\sVLANs:\s*(?P<op_trunk_allowed_vlan>.*)\n"
        r"^\s*Administrative\sTrunk\sUntagged\sVLANs:\s*(?P<adm_trunk_untagged_vlan>.*)\n"
        r"^\s*Operational\sTrunk\sUntagged\sVLANs:\s*(?P<op_trunk_untagged_vlan>.*)",
        re.MULTILINE,
    )
    rx_vlan2 = re.compile(
        r"^VLAN ID:\s+(?P<vlan_id>\d+)\s*\n"
        r"^Name:\s+\S+\s*\n"
        r"^State:\s+active\s*\n"
        r"^Status:\s+static\s*\n"
        r"^Member-Port:\s+port-list(?P<ports>\S+)\s*\n"
        r"^Untag-Ports:(\s+port-list(?P<untagged>\S+))?\s*\n",
        re.MULTILINE,
    )

    rx_vlans_ip = re.compile(r"^\s*(?P<iface>\d+)\s+(?P<vlan_id>\d+|none)", re.MULTILINE)
    rx_iface = re.compile(
        r"^\s*(?P<iface>\d+)\s+(?P<ip>\d\S+)\s+(?P<mask>\d\S+)\s+"
        r"(?P<vid>\d+)\s+(?P<oper_status>\S+)\s*\n",
        re.MULTILINE,
    )
    rx_iface2 = re.compile(
        r"^\s*(?P<iface>\d+)\s+(?P<ip>\d\S+)\s+(?P<mask>\d\S+)\s+" r"assigned\s+primary\s*\n",
        re.MULTILINE,
    )
    rx_lldp = re.compile(
        r"LLDP enable status:\s+enable.+\n" r"LLDP enable ports:\s+(?P<ports>\S+)\n", re.MULTILINE
    )
    rx_lldp_iscom2624g = re.compile(r"^(?P<ifname>\S+)\s+enable\s+\S+\s*\n", re.MULTILINE)
    rx_descr = re.compile(r"^\s*(?P<port>port\d+)\s+(?P<descr>.+)\n", re.MULTILINE)
    rx_iface_description = re.compile(
        r"^\s*(?P<iface>\S+)\s+(?P<admin_status>UP|DOWN)\s+"
        r"(?P<oper_status>UP|DOWN)\s+(?P<descr>.+)\n",
        re.MULTILINE,
    )
    rx_iface_iscom2624g = re.compile(
        r"^\s*(?P<ifname>\S+) is (?P<oper_status>UP|DOWN), "
        r"administrative status is (?P<admin_status>UP|DOWN)\s*\n"
        r"(^\s*Description is \"(?P<descr>.+)\",?\s*\n)?"
        r"(^\s*Hardware is (?P<hw_type>\S+), MAC address is (?P<mac>\S+)\s*\n)?"
        r"(^\s*Internet Address is (?P<ip>\S+)\s+primary\s*\n)?"
        r"(^\s*Internet v6 Address is (?P<ipv6>\S+)\s+Link\s*\n)?"
        r"(^\s*MTU (?P<mtu>\d+) bytes\s*\n)?",
        re.MULTILINE,
    )
    rx_ifunit = re.compile(r"\D+(?P<ifunit>\d+\S*)")

    IFTYPES = {
        "gigaethernet": "physical",
        "fastethernet": "physical",
        "vlan-interface": "SVI",
        "null": "null",
        "loopback": "loopback",
        "trunk": "aggregated",
        "unknown": "unknown",
    }

    def parse_vlans(self, section):
        r = {}
        match = self.rx_vlans.search(section)
        if match:
            r = match.groupdict()
        return r

    def execute_iscom2624g(self):
        lldp_ifaces = []
        v = self.cli("show lldp local config")
        lldp_ifaces_raw = self.rx_lldp_iscom2624g.findall(v)
        for iface in lldp_ifaces_raw:
            lldp_ifaces += [self.profile.convert_interface_name(iface)]
        ifaces = []
        v = self.cli("show interface")
        for iface in v.split("\n\n"):
            if not iface:
                continue
            match = self.rx_iface_iscom2624g.search("%s\n" % iface)
            ifname = match.group("ifname")
            if match.group("hw_type"):
                hw_type = match.group("hw_type")
                if ifname.startswith("NULL") and hw_type == "unknown":
                    hw_type = "null"
            else:
                if ifname.startswith("loopback"):
                    hw_type = "loopback"
            i = {
                "name": ifname,
                "type": self.profile.get_interface_type(ifname),
                "admin_status": match.group("admin_status") == "UP",
                "oper_status": match.group("oper_status") == "UP",
            }
            sub = {
                "name": ifname,
                "admin_status": match.group("admin_status") == "UP",
                "oper_status": match.group("oper_status") == "UP",
                "enabled_afi": [],
            }
            if match.group("descr"):
                i["description"] = match.group("descr").strip('"')
                sub["description"] = match.group("descr").strip('"')
            if match.group("mac") and match.group("mac") != "0000.0000.0000":
                i["mac"] = match.group("mac")
                sub["mac"] = match.group("mac")
            if match.group("mtu"):
                sub["mtu"] = match.group("mtu")
            if match.group("ip"):
                sub["ipv4_addresses"] = [match.group("ip")]
                sub["enabled_afi"] += ["IPv4"]
            if match.group("ipv6"):
                sub["ipv6_addresses"] = [match.group("ipv6")]
                sub["enabled_afi"] += ["IPv6"]
            if i["type"] == "physical":
                sub["enabled_afi"] += ["BRIDGE"]
                if ifname in lldp_ifaces:
                    i["enabled_protocols"] = ["LLDP"]
                match = self.rx_ifunit.search(ifname)
                ifunit = match.group("ifunit")
                try:
                    v = self.cli("show switchport interface %s %s" % (hw_type, ifunit))
                    vlans = self.parse_vlans(v)
                    if vlans["op_mode"] != "trunk":
                        sub["untagged_vlan"] = int(vlans["untagged_vlan"])
                    else:
                        sub["untagged_vlan"] = int(vlans["trunk_native_vlan"])
                        sub["tagged_vlans"] = self.expand_rangelist(vlans["op_trunk_allowed_vlan"])
                except self.CLISyntaxError:
                    pass
            if i["type"] == "SVI":
                match = self.rx_ifunit.search(ifname)
                ifunit = match.group("ifunit")
                sub["vlan_ids"] = [int(ifunit)]
            i["subinterfaces"] = [sub]
            ifaces += [i]
        return [{"interfaces": ifaces}]

    def execute_cli(self):
        if self.is_iscom2624g:
            return self.execute_iscom2624g()
        lldp_ifaces = []
        v = self.cli("show lldp local config")
        match = self.rx_lldp.search(v)
        if match:
            lldp_ifaces = self.expand_rangelist(match.group("ports"))
        ifaces = []
        v = self.cli("show interface port description")
        for line in v.splitlines()[2:-1]:
            i = {
                "name": int(line[:8]),
                "type": "physical",
                "snmp_ifindex": int(line[:8]),
                "subinterfaces": [],
            }
            if str(line[8:]) != "-":
                i["description"] = str(line[8:])
            if i["name"] in lldp_ifaces:
                i["enabled_protocols"] = ["LLDP"]
            ifaces.append(i)
        statuses = []
        v = self.cli("show interface port")
        for line in v.splitlines()[5:]:
            i = {
                "name": int(line[:6]),
                "admin_status": "enable" in line[7:14],
                "oper_status": "up" in line[14:29],
            }
            statuses.append(i)
        vlans = []
        v = self.cli("show interface port switchport")
        for section in v.split("Port"):
            if not section:
                continue
            vlans.append(self.parse_vlans(section))
        d = defaultdict(dict)

        for l in (statuses, ifaces):
            for elem in l:
                d[elem["name"]].update(elem)
        l3 = list(six.itervalues(d))

        for port in l3:
            name = port["name"]
            port["subinterfaces"] = [
                {
                    "name": str(name),
                    "enabled_afi": ["BRIDGE"],
                    "admin_status": port["admin_status"],
                    "oper_status": port["oper_status"],
                    "tagged_vlans": [],
                    "untagged_vlan": [
                        int(vlan["untagged_vlan"]) for vlan in vlans if int(vlan["name"]) == name
                    ][0],
                }
            ]
            if "description" in port:
                port["subinterfaces"][0]["description"] = port["description"]
            tvl = [vlan["op_trunk_allowed_vlan"] for vlan in vlans if int(vlan["name"]) == name][0]
            if "n/a" not in tvl:
                port["subinterfaces"][0]["tagged_vlans"] = ranges_to_list(tvl)
        if_descr = []
        v = self.cli("show interface ip description")
        for line in v.splitlines()[2:-1]:
            i = {"name": int(line[:9]), "description": str(line[9:])}
            if_descr.append(i)
        if not l3:
            v = self.cli("show interface description")
            for match in self.rx_descr.finditer(v):
                i = {
                    "name": match.group("port"),
                    "type": "physical",
                    "description": match.group("descr").strip(),
                    "enabled_protocols": [],
                    "subinterfaces": [
                        {"name": match.group("port"), "description": match.group("descr").strip()}
                    ],
                }
                l3 += [i]
            v = self.cli("show vlan detail")
            for match in self.rx_vlan2.finditer(v):
                vlan_id = int(match.group("vlan_id"))
                ports = ranges_to_list(match.group("ports"))
                if match.group("untagged"):
                    untagged = ranges_to_list(match.group("untagged"))
                else:
                    untagged = []
                for i in l3:
                    for p in ports:
                        if i["name"] == "port%s" % p:
                            if p not in untagged:
                                if "tagged_vlans" in i["subinterfaces"][0]:
                                    i["subinterfaces"][0]["tagged_vlans"] += [vlan_id]
                                else:
                                    i["subinterfaces"][0]["tagged_vlans"] = [vlan_id]
                            else:
                                i["subinterfaces"][0]["untagged_vlan"] = vlan_id
        v = self.profile.get_version(self)
        mac = v["mac"]
        # XXX: This is a dirty hack !!!
        # I do not know, how get ip interface MAC address
        try:
            v = self.cli("show interface ip")
        except self.CLISyntaxError:
            v = self.cli("show interface ip 0")
        for match in self.rx_iface.finditer(v):
            ifname = match.group("iface")
            i = {
                "name": "ip%s" % ifname,
                "type": "SVI",
                "oper_status": match.group("oper_status") == "active",
                "admin_status": match.group("oper_status") == "active",
                "mac": mac,
                "enabled_protocols": [],
                "subinterfaces": [
                    {
                        "name": "ip%s" % ifname,
                        "oper_status": match.group("oper_status") == "active",
                        "admin_status": match.group("oper_status") == "active",
                        "mac": mac,
                        "vlan_ids": [int(match.group("vid"))],
                        "enabled_afi": ["IPv4"],
                    }
                ],
            }
            addr = match.group("ip")
            mask = match.group("mask")
            ip_address = "%s/%s" % (addr, IPv4.netmask_to_len(mask))
            i["subinterfaces"][0]["ipv4_addresses"] = [ip_address]
            for q in if_descr:
                if str(q["name"]).strip() == ifname:
                    i["description"] = q["description"]
                    i["subinterfaces"][0]["description"] = q["description"]
            l3 += [i]
        try:
            v = self.cli("show ip interface brief")
        except self.CLISyntaxError:
            return [{"interfaces": l3}]
        for match in self.rx_iface2.finditer(v):
            ifname = match.group("iface")
            i = {
                "name": "ip%s" % ifname,
                "type": "SVI",
                "mac": mac,
                "enabled_protocols": [],
                "subinterfaces": [{"name": "ip%s" % ifname, "mac": mac, "enabled_afi": ["IPv4"]}],
            }
            addr = match.group("ip")
            mask = match.group("mask")
            ip_address = "%s/%s" % (addr, IPv4.netmask_to_len(mask))
            i["subinterfaces"][0]["ipv4_addresses"] = [ip_address]
            l3 += [i]
        v = self.cli("show interface ip vlan")
        for match in self.rx_vlans_ip.finditer(v):
            vlan_id = match.group("vlan_id")
            if vlan_id == "none":
                continue
            ifname = "ip%s" % match.group("iface")
            for i in l3:
                if i["name"] == ifname:
                    i["subinterfaces"][0]["vlan_ids"] = vlan_id
                    break
        return [{"interfaces": l3}]
