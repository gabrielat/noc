# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# rename DES2108
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.execute(
            """
        UPDATE sa_managedobject
        SET profile_name='DLink.DES21xx'
        WHERE profile_name='DLink.DES2108'"""
        )
