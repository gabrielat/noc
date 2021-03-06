# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Brocade.ADX.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion


class Script(BaseScript):
    name = "Brocade.ADX.get_version"
    cache = True
    interface = IGetVersion

    rx_ver = re.compile(
        r"System Version (?P<version>[^\s,]+)\s(?:.*)"
        r"Type\:\s+(?P<platform>.+?)"
        r"(?:\s+Backplane Serial .+)",
        re.MULTILINE | re.DOTALL,
    )

    rx_snmp_ver = re.compile(
        r"^(?:Brocade Communications Systems, Inc.) (?P<platform>.+?) "
        r"TrafficWork Version (?P<version>[^,]+)"
    )

    def execute(self):
        if self.snmp and self.access_profile.snmp_ro:
            try:
                # sysDescr.0
                v = self.snmp.get("1.3.6.1.2.1.1.1.0", cached=True)
                if v:
                    match = self.re_search(self.rx_snmp_ver, v)
                    platform = match.group("platform")
                    return {
                        "vendor": "Brocade",
                        "platform": match.group("platform"),
                        "version": match.group("version"),
                    }
            except self.snmp.TimeOutError:
                pass
        v = self.cli("show version", cached=True)
        match = self.re_search(self.rx_ver, v)
        platform = match.group("platform")
        return {"vendor": "Brocade", "platform": platform, "version": match.group("version")}
