# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Qtech.QSW2800.SlotRule
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

from noc.sa.profiles.Generic.get_metrics import OIDRule
from noc.core.mib import mib


class SlotRule(OIDRule):

    name = "slot"

    def iter_oids(self, script, metric):
        i = 1
        r = {}
        if script.has_capability("Stack | Member Ids"):
            sysSlotIndex = [
                int(index) for index in script.capabilities["Stack | Member Ids"].split(" | ")
            ]
        elif script.has_capability("Stack | Members"):
            sysSlotIndex = list(range(1, script.capabilities["Stack | Members"] + 1))
        else:
            sysSlotIndex = [1]

        for ms in sysSlotIndex:
            r[str(i)] = "%d" % ms
            # r[str(i)] = {"healthModuleSlot": ms}
            i += 1

        for i in r:
            if self.is_complex:
                gen = [mib[self.expand(o, {"hwSlotIndex": r[i]})] for o in self.oid]
                path = ["0", "0", i, ""] if "CPU" in metric.metric else ["0", i, "0"]
                if gen:
                    yield tuple(gen), self.type, self.scale, path
            else:
                oid = mib[self.expand(self.oid, {"hwSlotIndex": r[i]})]
                path = ["0", "0", i, ""] if "CPU" in metric.metric else ["0", i, "0"]
                if oid:
                    yield oid, self.type, self.scale, path
