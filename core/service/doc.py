# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Service documentation request handler
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import tornado.web


class DocRequestHandler(tornado.web.RequestHandler):
    def initialize(self, service):
        self.service = service

    def get(self):
        r = ["%s documentation" % self.service.name]
        for s in self.service.api:
            r += [s.__doc__]
            for m in dir(s):
                h = getattr(s, m)
                if hasattr(h, "api"):
                    r += [m]
                    r += [h.__doc__]
        self.write("\n".join(r))
