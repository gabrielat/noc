# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Eltex.WOP.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
import six

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces
from noc.core.ip import IPv4


class Script(BaseScript):
    name = "Eltex.WOP.get_interfaces"
    cache = True
    interface = IGetInterfaces

    BLOCK_SPLITTER = "-" * 15
    BSS_DESCRIPTION_TEMPLATE = (
        "ssid_broadcast=%s, ieee_mode=%s, channel=%s, freq=%s, channelbandwidth=%sMHz"
    )

    FREQ = {"bg-n": "2400GHz", "a-n": "5150GHz"}

    @classmethod
    def get_interface_freq(cls, name):
        c = cls.FREQ.get(name)
        return c

    IEEE = {"bg-n": "IEEE 802.11b/g/n", "a-n": "IEEE 802.11a/n"}

    @classmethod
    def get_interface_ieee(cls, name):
        c = cls.IEEE.get(name)
        return c

    def get_radio_detail(self):
        r = {}
        w = self.cli("get radio all detail")

        for block in w.split("\n\n"):
            if not block:
                continue
            value = self.profile.table_parser(block)
            if "name" in value:
                r[value["name"]] = {
                    "ieee_mode": self.get_interface_ieee(value["mode"]),
                    "channel": value["channel"],
                    "freq": self.get_interface_freq(value["mode"]),
                    "channelbandwidth": value["n-bandwidth"]
                    if "n-bandwidth" in value
                    else value["bandwidth"],
                }
        return r

    def get_bss_detail(self, bss):
        v = self.cli("get bss %s detail" % bss)
        value = self.profile.table_parser(v)
        if value.get("radio"):
            return value

    def execute_cli(self, **kwargs):
        interfaces = {}
        wres = self.get_radio_detail()

        c = self.cli("get interface all detail")
        for block in c.split("\n\n"):
            value = self.profile.table_parser(block)
            if "name" not in value:
                self.logger.info("Ignoring unknown interface: '%s", value)
                continue
            ip_address = None
            ifname = value["name"]
            interfaces[ifname] = {
                "type": self.profile.get_interface_type(ifname),
                "name": ifname,
                "subinterfaces": [],
            }
            if value["mac"]:
                interfaces[ifname]["mac"] = value["mac"]
            if "eth" in ifname:
                interfaces[ifname]["subinterfaces"] += [
                    {"name": ifname, "mac": value["mac"], "enabled_afi": ["BRIDGE"]}
                ]
            # static-ip or "ip" field may use
            if value.get("static-ip"):
                ip_address = "%s/%s" % (
                    value["static-ip"],
                    IPv4.netmask_to_len(value.get("static-mask") or "255.255.255.255"),
                )
            elif value.get("ip") in value:
                ip_address = "%s/%s" % (
                    value["ip"],
                    IPv4.netmask_to_len(value.get("mask") or "255.255.255.255"),
                )
            if ip_address:
                interfaces[ifname]["subinterfaces"] += [
                    {
                        "name": ifname,
                        "mac": value["mac"],
                        "enabled_afi": ["IPv4"],
                        "ipv4_addresses": [ip_address],
                    }
                ]
            if value.get("bss") and value.get("ssid"):
                # For some reason creating SSID as interfaces otherwise sub.
                interfaces.pop(ifname)
                ssid = value["ssid"].replace(" ", "").replace("Managed", "")
                if ssid.startswith("2a2d"):
                    # 2a2d - hex string
                    ssid = ssid.decode("hex")
                r = self.get_bss_detail(value["bss"])
                bss_ifname = "%s.%s" % (ifname, ssid)
                if r:
                    radio = wres[r["radio"]]
                    interfaces[bss_ifname] = {
                        "type": "physical",
                        "name": bss_ifname,
                        "mac": value["mac"],
                        "description": self.BSS_DESCRIPTION_TEMPLATE
                        % (
                            "Enable" if r["ignore-broadcast-ssid"] == "off" else "Disable",
                            radio["ieee_mode"],
                            radio["channel"],
                            radio["freq"],
                            radio["channelbandwidth"],
                        ),
                        "subinterfaces": [
                            {
                                "name": "%s.%s" % (ifname, ssid),
                                "mac": value["mac"],
                                "enabled_afi": ["BRIDGE"],
                            }
                        ],
                    }
        return [{"interfaces": list(six.itervalues(interfaces))}]
