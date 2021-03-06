# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Middleware loader
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# NOC modules
from noc.core.loader.base import BaseLoader
from .base import BaseMiddleware


class MiddlewareLoader(BaseLoader):
    name = "middleware"
    base_cls = BaseMiddleware
    base_path = ("core", "script", "http", "middleware")


loader = MiddlewareLoader()
