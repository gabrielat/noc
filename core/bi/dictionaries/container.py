# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Container dictionary
# ----------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.clickhouse.dictionary import Dictionary
from noc.core.clickhouse.fields import StringField, ReferenceField


class Container(Dictionary):
    class Meta(object):
        name = "container"
        layout = "hashed"

    id = StringField()
    name = StringField()
    parent = ReferenceField("self")
    address_text = StringField()
