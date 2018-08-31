# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# TTSystem loader
# ----------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
# NOC modules
from .base import BaseLoader
from noc.fm.models.ttsystem import TTSystem


class TTMapLoader(BaseLoader):
    name = "ttsystem"
    model = TTSystem
    fields = [
        "id",
        "name",
        "handler",
        "connection",
        "description"
    ]
