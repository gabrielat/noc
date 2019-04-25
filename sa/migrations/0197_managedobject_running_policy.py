# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ManagedObjectProfile discovery running policy
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
from django.db import models


class Migration(object):
    def forwards(self):
        db.add_column(
            "sa_managedobjectprofile", "box_discovery_running_policy",
            models.CharField(
                "Box Running Policy",
                choices=[("R", "Require Up"), ("r", "Require if enabled"), ("i", "Ignore")],
                max_length=1,
                default="R"
            )
        )
        db.add_column(
            "sa_managedobjectprofile", "periodic_discovery_running_policy",
            models.CharField(
                "Periodic Running Policy",
                choices=[("R", "Require Up"), ("r", "Require if enabled"), ("i", "Ignore")],
                max_length=1,
                default="R"
            )
        )
        db.add_column(
            "sa_managedobject", "box_discovery_running_policy",
            models.CharField(
                "Box Running Policy",
                choices=[("P", "From Profile"), ("R", "Require Up"), ("r", "Require if enabled"), ("i", "Ignore")],
                max_length=1,
                default="P"
            )
        )
        db.add_column(
            "sa_managedobject", "periodic_discovery_running_policy",
            models.CharField(
                "Periodic Running Policy",
                choices=[("P", "From Profile"), ("R", "Require Up"), ("r", "Require if enabled"), ("i", "Ignore")],
                max_length=1,
                default="P"
            )
        )

    def backwards(self):
        pass