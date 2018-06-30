# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Huawei.VRP3.get_ifindexes
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetifindexes import IGetIfindexes
from noc.sa.interfaces.base import InterfaceTypeError
from noc.core.mib import mib


class Script(BaseScript):
    name = "Huawei.VRP3.get_ifindexes"
    interface = IGetIfindexes
    cache = True
    requires = []

    MAX_GETNEXT_RETIRES = 0
    INTERFACE_NAME_OID = "IF-MIB::ifName"

    def get_getnext_retires(self):
        return self.MAX_GETNEXT_RETIRES

    def execute_snmp(self, name_oid=INTERFACE_NAME_OID):
        r = {}
        unknown_interfaces = []
        for oid, name in self.snmp.getnext(mib[name_oid],
                                           max_retries=self.get_getnext_retires()):
            try:
                v = self.profile.convert_interface_name(name)
            except InterfaceTypeError as e:
                self.logger.debug(
                    "Ignoring unknown interface %s: %s",
                    name, e
                )
                unknown_interfaces += [name]
                continue
            ifindex = int(oid.split(".")[-1])
            r[v] = ifindex
        if unknown_interfaces:
            self.logger.info("%d unknown interfaces has been ignored",
                             len(unknown_interfaces))
        return r
