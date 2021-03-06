# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Card search
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# Third-party modules
import tornado.web
import ujson

# NOC modules
from noc.sa.models.useraccess import UserAccess
from .card import CardRequestHandler


class SearchRequestHandler(CardRequestHandler):
    def get(self, *args, **kwargs):
        scope = self.get_argument("scope")
        query = self.get_argument("query")
        card = self.CARDS.get(scope)
        if not card or not hasattr(card, "search"):
            raise tornado.web.HTTPError(404)
        result = card.search(self, query)
        self.set_header("Content-Type", "application/json")
        self.write(ujson.dumps(result))

    def get_user_domains(self):
        return UserAccess.get_domains(self.current_user)
