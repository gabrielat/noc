# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# ArchivedEvent model
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# Third-party modules
from mongoengine.document import Document
from mongoengine.fields import (
    DateTimeField,
    IntField,
    DictField,
    ListField,
    EmbeddedDocumentField,
    ObjectIdField,
)
from django.template import Template, Context
import six

# NOC modules
from noc.sa.models.managedobject import ManagedObject
from noc.core.mongo.fields import ForeignKeyField, PlainReferenceField, RawDictField
from .eventlog import EventLog
from .eventclass import EventClass


@six.python_2_unicode_compatible
class ArchivedEvent(Document):
    meta = {
        "collection": "noc.events.archive",
        "strict": False,
        "auto_create_index": False,
        "indexes": ["timestamp", "alarms"],
    }
    status = "S"

    timestamp = DateTimeField(required=True)
    managed_object = ForeignKeyField(ManagedObject, required=True)
    event_class = PlainReferenceField(EventClass, required=True)
    start_timestamp = DateTimeField(required=True)
    repeats = IntField(required=True)
    raw_vars = RawDictField()
    resolved_vars = RawDictField()
    vars = DictField()
    log = ListField(EmbeddedDocumentField(EventLog))
    alarms = ListField(ObjectIdField())

    def __str__(self):
        return "%s" % self.id

    @property
    def duration(self):
        """
        Logged event duration in seconds
        """
        return (self.timestamp - self.start_timestamp).total_seconds()

    def get_template_vars(self):
        """
        Prepare template variables
        """
        vars = self.vars.copy()
        vars.update({"event": self})
        return vars

    @property
    def subject(self):
        ctx = Context(self.get_template_vars())
        s = Template(self.event_class.subject_template).render(ctx)
        if len(s) >= 255:
            s = s[:125] + " ... " + s[-125:]
        return s

    @property
    def body(self):
        ctx = Context(self.get_template_vars())
        s = Template(self.event_class.body_template).render(ctx)
        return s
