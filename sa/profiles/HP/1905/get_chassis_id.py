# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# HP.1905.get_chassis_id
# ---------------------------------------------------------------------
# Copyright (C) 2007-2013 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetchassisid import IGetChassisID


class Script(BaseScript):
    name = "HP.1905.get_chassis_id"
    interface = IGetChassisID
    cache = True

    def execute(self):
        # Try SNMP first
        if self.has_snmp():
            try:
                mac = self.snmp.get("1.3.6.1.2.1.2.2.1.6.3718", cached=True)
                return {"first_chassis_mac": mac, "last_chassis_mac": mac}
            except self.snmp.TimeOutError:
                pass

        # Fallback to CLI
        raise Exception("Not implemented")
