# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# event indexes
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.create_index("fm_event", ["status"])
        self.db.create_index("fm_event", ["timestamp"])
