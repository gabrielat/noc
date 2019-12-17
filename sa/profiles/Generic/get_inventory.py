# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Generic.get_inventory
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinventory import IGetInventory


class Script(BaseScript):
    name = "Generic.get_inventory"
    interface = IGetInventory

    def execute_snmp(self):
        v = self.scripts.get_version()
        if "attributes" in v and v["attributes"]["Serial Number"]:
            serial = v["attributes"]["Serial Number"]

        return [
            {
                "type": "CHASSIS",
                "vendor": [v["vendor"]],
                "part_no": [v["platform"]],
                "serial": serial,
            }
        ]
