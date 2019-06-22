# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Pretty command
# ----------------------------------------------------------------------
#  Copyright (C) 2007-2019 The NOC Project
#  See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.runner import MigrationRunner
from noc.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Perform database migrations
    """
    help = "migrate database"

    def handle(self, *args, **options):
        runner = MigrationRunner()
        runner.migrate()


if __name__ == "__main__":
    Command().run()
