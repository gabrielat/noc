#!./bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Activator service
# ----------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.service.base import Service
from noc.services.activator.api.activator import ActivatorAPI


class ActivatorService(Service):
    name = "activator"
    pooled = True
    api = [ActivatorAPI]
    process_name = "noc-%(name).10s-%(pool).5s"
    use_telemetry = True

    def __init__(self):
        super(ActivatorService, self).__init__()


if __name__ == "__main__":
    ActivatorService().start()
