# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# H3C.VRP.get_chassis_id
# ---------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetchassisid import IGetChassisID
from noc.core.mac import MAC


class Script(BaseScript):
    name = "H3C.VRP.get_chassis_id"
    cache = True
    interface = IGetChassisID

    rx_mac_old = re.compile(r"MAC address[^:]*?:\s*(?P<id>\S+)", re.IGNORECASE | re.MULTILINE)

    @BaseScript.match(version__startswith="3.02")
    def execute_old(self):
        v = self.cli("display stp")
        match = self.rx_mac_old.search(v)
        mac = match.group("id")
        return {"first_chassis_mac": mac, "last_chassis_mac": mac}

    rx_mac = re.compile(r"^CIST Bridge[^:]*?:\s*\d+?\.(?P<id>\S+)", re.IGNORECASE | re.MULTILINE)

    rx_mac1 = re.compile(r"^\s*MAC(_|\s)ADDRESS[^:]*?:\s(?P<id>\S+)", re.IGNORECASE | re.MULTILINE)

    @BaseScript.match()
    def execute_new(self):
        shift = 0
        if self.match_version(platform__contains="S3600"):
            # S3600 platform has additional MAC address for L3
            shift = 1
        v = self.cli("display stp")
        match = self.rx_mac.search(v)
        if match is not None:
            mac = match.group("id")
        else:
            v = self.cli("display device manuinfo")
            match = self.rx_mac1.search(v)
            mac = match.group("id")
        if shift:
            last_mac = str(MAC(mac).shift(shift))
        else:
            last_mac = mac
        return {"first_chassis_mac": mac, "last_chassis_mac": last_mac}
