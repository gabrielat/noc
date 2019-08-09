# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ConfDBQuery model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import threading
import operator
import os

# Third-party modules
from mongoengine.document import Document
from mongoengine.fields import StringField, UUIDField, BooleanField
import six
import cachetools

# NOC modules
from noc.lib.prettyjson import to_json
from noc.lib.text import quote_safe_path
from noc.core.model.decorator import on_delete_check

id_lock = threading.Lock()


@on_delete_check(
    check=[
        ("cm.ObjectValidationPolicy", "filer_query"),
        ("cm.ObjectValidationPolicy", "rules.query"),
        ("cm.ObjectValidationPolicy", "rules.filer_query"),
    ]
)
@six.python_2_unicode_compatible
class ConfDBQuery(Document):
    meta = {
        "collection": "confdbqueries",
        "strict": True,
        "auto_create_index": False,
        "json_collection": "cm.confdbqueries",
        "json_unique_fields": ["name"],
    }

    name = StringField(unique=True)
    uuid = UUIDField(binary=True)
    description = StringField()
    source = StringField()
    allow_object_filter = BooleanField(default=False)
    allow_interface_filter = BooleanField(default=False)
    allow_object_validation = BooleanField(default=False)
    allow_interface_validation = BooleanField(default=False)
    allow_object_classification = BooleanField(default=False)
    allow_interface_classification = BooleanField(default=False)

    _id_cache = cachetools.TTLCache(maxsize=100, ttl=60)

    def __str__(self):
        return self.name

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_by_id(cls, id):
        return ConfDBQuery.objects.filter(id=id).first()

    def get_json_path(self):
        p = [quote_safe_path(n.strip()) for n in self.name.split("|")]
        return os.path.join(*p) + ".json"

    def query(self, engine, **kwargs):
        """
        Run query against ConfDB engine
        :param engine: ConfDB engine
        :param kwargs: Optional arguments
        :return:
        """
        for ctx in engine.query(self.source, **kwargs):
            yield ctx

    def any(self, engine, **kwargs):
        """
        Run query agains ConfDB engine and return True if any result found
        :param engine: ConfDB engine
        :param kwargs: Optional arguments
        :return: True if any result found
        """
        return engine.any(self.source, **kwargs)

    def to_json(self):
        r = {
            "name": self.name,
            "$collection": self._meta["json_collection"],
            "uuid": self.uuid,
            "source": self.source,
            "allow_object_filter": self.allow_object_filter,
            "allow_interface_filter": self.allow_interface_filter,
            "allow_object_validation": self.allow_object_validation,
            "allow_interface_validation": self.allow_interface_validation,
            "allow_object_classification": self.allow_object_classification,
            "allow_interface_classification": self.allow_interface_classification,
        }
        if self.description:
            r["description"] = self.description
        return to_json(
            r,
            order=[
                "name",
                "$collection",
                "uuid",
                "description",
                "source",
                "allow_object_filter",
                "allow_interface_filter",
                "allow_object_validation",
                "allow_interface_validation",
                "allow_object_classification",
                "allow_interface_classification",
            ],
        )
