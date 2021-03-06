# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Version dictionary
# ----------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.clickhouse.dictionary import Dictionary
from noc.core.clickhouse.fields import StringField


class Version(Dictionary):
    class Meta(object):
        name = "version"
        layout = "flat"

    name = StringField()
    profile = StringField()
    vendor = StringField()
