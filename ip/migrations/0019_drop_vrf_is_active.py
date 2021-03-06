# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Drop VRF.is_active
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.delete_column("ip_vrf", "is_active")
