# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# URLSession middleware
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# NOC modules
from .base import BaseMiddleware


class URLSessionMiddleware(BaseMiddleware):
    """
    Append &session_id=XXXXX to requests.
    `session_id` name may be changed via `session_param`
    """

    name = "urlsession"

    def __init__(self, http, session_param="session_id"):
        super(URLSessionMiddleware, self).__init__(http)
        self.session_param = session_param

    def process_request(self, url, body, headers):
        if self.http.session_id:
            if "?" in url:
                url += "&%s=%s" % (self.session_param, self.http.session_id)
            else:
                url += "?%s=%s" % (self.session_param, self.http.session_id)
        return url, body, headers
