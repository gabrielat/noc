# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Enumeration model
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
import six
from mongoengine.document import Document
from mongoengine.fields import StringField, DictField, UUIDField

# Python modules
from noc.core.text import quote_safe_path
from noc.core.prettyjson import to_json


@six.python_2_unicode_compatible
class Enumeration(Document):
    meta = {
        "collection": "noc.enumerations",
        "strict": False,
        "auto_create_index": False,
        "json_collection": "fm.enumerations",
        "json_unique_fields": ["name"],
    }

    name = StringField(unique=True)
    uuid = UUIDField(binary=True)
    values = DictField()  # value -> [possible combinations]

    def __str__(self):
        return self.name

    def get_json_path(self):
        return "%s.json" % quote_safe_path(self.name)

    def to_json(self):
        return to_json(
            {
                "name": self.name,
                "$collection": self._meta["json_collection"],
                "uuid": self.uuid,
                "values": self.values,
            },
            order=["name", "$collection", "uuid"],
        )
