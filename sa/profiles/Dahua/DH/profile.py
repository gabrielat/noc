# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Vendor: Dahua
# OS:     DH
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "Dahua.DH"
    enable_http_session = True
    http_request_middleware = ["digestauth"]

    rx_depth = re.compile(r"\S+(\[[\S\d]+\])")

    @staticmethod
    def parse_equal_output(string):
        r = dict(l.split("=", 1) for l in string.splitlines())
        return r

    def parse_tokens(self, string):
        for line in string.splitlines():
            key, value = line.split("=")
            path = []
            for p in key.split("."):
                if self.rx_depth.match(p):
                    p1, p2 = p.split("[", 1)
                    p2 = [int(x.strip("[]")) for x in p2.split("][")]
                else:
                    p1, p2 = p, []
                path += [p1]
                path += p2
            yield path, value