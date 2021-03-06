# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Sun.iLOM3.get_config
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetconfig import IGetConfig


class Script(BaseScript):
    name = "Sun.iLOM3.get_config"
    interface = IGetConfig

    def execute_cli(self, **kwargs):
        self.cli("cd /SP/config")
        with self.servers.ftp() as ftp:
            url = ftp.get_url(self.access_profile.address)
            self.cli("dump -destination %s" % url)
            config = ftp.get_data()
        self.cli("cd /")
        return self.cleaned_config(config)
