# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# dnsserver generator_name
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from django.db import models

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.add_column(
            "dns_dnsserver",
            "generator_name",
            models.CharField("Generator", max_length=32, default="BINDv9"),
        )
        self.db.execute("UPDATE dns_dnsserver SET generator_name=%s", ["BINDv9"])
