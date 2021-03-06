# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# DLink.DxS_Cisco_CLI.get_interface_status
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfacestatus import IGetInterfaceStatus


class Script(BaseScript):
    name = "DLink.DxS_Cisco_CLI.get_interface_status"
    interface = IGetInterfaceStatus
    rx_line = re.compile(
        r"^(?P<interface>\S+\s*\d+(\/\d+)?)\s+(?P<status>up|down)\s+\d+\s+"
        r"(Unknown|Half|Full)\s+\S+\s+(copper|fiber)\s*$",
        re.IGNORECASE | re.MULTILINE,
    )

    def execute(self, interface=None):
        # Not tested. Must be identical in different vendors
        if self.has_snmp():
            try:
                # Get interface status
                r = []
                # IF-MIB::ifName, IF-MIB::ifOperStatus
                for n, s in self.snmp.join_tables("1.3.6.1.2.1.31.1.1.1.1", "1.3.6.1.2.1.2.2.1.8"):
                    # ifOperStatus up(1)
                    r += [{"interface": n, "status": int(s) == 1}]
                return r
            except self.snmp.TimeOutError:
                pass
        # Fallback to CLI
        r = []
        for match in self.rx_line.finditer(self.cli("show interfaces status")):
            r += [
                {
                    "interface": match.group("interface"),
                    "status": match.group("status").lower() == "up",
                }
            ]
        return r
