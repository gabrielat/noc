# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# configrevisions API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# Third-party modules
import tornado.gen
import ujson
import six

# NOC modules
from noc.core.service.apiaccess import authenticated
from noc.sa.models.managedobject import ManagedObject
from ..base import NBIAPI


class ConfigRevisionsAPI(NBIAPI):
    name = "configrevisions"

    @authenticated
    @tornado.gen.coroutine
    def get(self, object_id):
        code, result = yield self.executor.submit(self.handler, object_id)
        self.set_status(code)
        if isinstance(result, six.string_types):
            self.write(result)
        else:
            self.set_header("Content-Type", "text/json")
            self.write(ujson.dumps(result))

    def handler(self, object_id):
        mo = ManagedObject.get_by_id(int(object_id))
        if not mo:
            return 404, "Not Found"
        revs = [
            {"revision": str(r.id), "timestamp": r.ts.isoformat()}
            for r in mo.config.get_revisions()
        ]
        return 200, revs

    @classmethod
    def get_path(cls):
        return r"%s/(\d+)" % cls.name
