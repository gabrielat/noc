# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ObjectProfile dictionary
# ----------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.clickhouse.dictionary import Dictionary
from noc.core.clickhouse.fields import StringField, UInt8Field


class ObjectProfile(Dictionary):
    class Meta(object):
        name = "objectprofile"
        layout = "flat"

    name = StringField()
    # ObjectProfile Level
    level = UInt8Field
