# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# EventClass model
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
import re
import os
from threading import Lock
import operator

# Third-party modules
import six
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import (
    StringField,
    BooleanField,
    IntField,
    ListField,
    DictField,
    ObjectIdField,
    EmbeddedDocumentField,
    UUIDField,
)
import cachetools

# NOC modules
from noc.core.mongo.fields import PlainReferenceField
from noc.core.escape import json_escape as q
from noc.core.text import quote_safe_path
from noc.core.handler import get_handler
from noc.core.model.decorator import on_delete_check
from .alarmclass import AlarmClass

id_lock = Lock()
handlers_lock = Lock()


@six.python_2_unicode_compatible
class EventClassVar(EmbeddedDocument):
    meta = {"strict": False}
    name = StringField(required=True)
    description = StringField(required=False)
    type = StringField(
        required=True,
        choices=[
            (x, x)
            for x in (
                "str",
                "int",
                "float",
                "ipv4_address",
                "ipv6_address",
                "ip_address",
                "ipv4_prefix",
                "ipv6_prefix",
                "ip_prefix",
                "mac",
                "interface_name",
                "oid",
            )
        ],
    )
    required = BooleanField(required=True)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.description == other.description
            and self.type == other.type
            and self.required == other.required
        )


@six.python_2_unicode_compatible
class EventDispositionRule(EmbeddedDocument):
    meta = {"strict": False}
    # Name, unique within event class
    name = StringField(required=True, default="dispose")
    # Python logical expression to check do the rules
    # applicable or not.
    condition = StringField(required=True, default="True")
    # Python logical expression to evaluate managed object
    managed_object = StringField(required=False)
    # What to do with disposed event:
    #    drop - delete and stop disposition
    #    ignore - stop disposition
    #    pyrule - execute pyrule
    #    raise - raise an alarm
    #    clear - clear alarm
    #
    action = StringField(
        required=True, choices=[(x, x) for x in ("drop", "ignore", "raise", "clear")]
    )
    # Applicable for actions: raise and clear
    alarm_class = PlainReferenceField(AlarmClass, required=False)
    # Additional condition. Raise or clear action
    # will be performed only if additional events occured during time window
    combo_condition = StringField(
        required=False,
        default="none",
        choices=[
            (x, x)
            for x in (
                # Apply action immediately
                "none",
                # Apply when event firing rate
                # exceeds combo_count times during combo_window
                "frequency",
                # Apply action if event followed by all combo events
                # in strict order
                "sequence",
                # Apply action if event followed by all combo events
                # in no specific order
                "all",
                # Apply action if event followed by any of combo events
                "any",
            )
        ],
    )
    # Time window for combo events in seconds
    combo_window = IntField(required=False, default=0)
    # Applicable for frequency.
    combo_count = IntField(required=False, default=0)
    # Applicable for sequence, all and any combo_condition
    combo_event_classes = ListField(
        PlainReferenceField("fm.EventClass"), required=False, default=[]
    )
    # event var name -> alarm var name mappings
    # try to use direct mapping if not set explicitly
    var_mapping = DictField(required=False)
    # Stop event disposition if True or continue with next rule
    stop_disposition = BooleanField(required=False, default=True)

    def __str__(self):
        return "%s: %s" % (self.action, self.alarm_class.name)

    def __eq__(self, other):
        for a in [
            "name",
            "condition",
            "action",
            "pyrule",
            "window",
            "var_mapping",
            "stop_disposition",
            "managed_object",
        ]:
            if hasattr(self, a) != hasattr(other, a):
                return False
            if hasattr(self, a) and getattr(self, a) != getattr(other, a):
                return False
        if self.alarm_class is None and other.alarm_class is None:
            return True
        if (
            self.alarm_class is None
            or other.alarm_class is None
            or self.alarm_class.name != other.alarm_class.name
        ):
            return False
        return True


@six.python_2_unicode_compatible
class EventSuppressionRule(EmbeddedDocument):
    meta = {"strict": False}
    name = StringField()
    condition = StringField(required=True, default="True")
    event_class = PlainReferenceField("fm.EventClass", required=True)
    match_condition = DictField(required=True, default={})
    window = IntField(required=True, default=3600)
    suppress = BooleanField(required=True, default=True)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.condition == other.condition
            and self.event_class.id == other.event_class.id
            and self.match_condition == other.match_condition
            and self.window == other.window
            and self.suppress == other.suppress
        )


@six.python_2_unicode_compatible
class EventPlugin(EmbeddedDocument):
    meta = {"strict": False}

    name = StringField()
    config = DictField(default={})

    def __str__(self):
        return self.name


@six.python_2_unicode_compatible
class EventClassCategory(Document):
    meta = {"collection": "noc.eventclasscategories", "strict": False, "auto_create_index": False}
    name = StringField()
    parent = ObjectIdField(required=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if " | " in self.name:
            p_name = " | ".join(self.name.split(" | ")[:-1])
            p = EventClassCategory.objects.filter(name=p_name).first()
            if not p:
                p = EventClassCategory(name=p_name)
                p.save()
            self.parent = p.id
        else:
            self.parent = None
        super(EventClassCategory, self).save(*args, **kwargs)


@on_delete_check(
    check=[
        ("fm.EventClassificationRule", "event_class"),
        ("fm.ArchivedEvent", "event_class"),
        ("fm.ActiveEvent", "event_class"),
    ]
)
@six.python_2_unicode_compatible
class EventClass(Document):
    """
    Event class
    """

    meta = {
        "collection": "noc.eventclasses",
        "strict": False,
        "auto_create_index": False,
        "json_collection": "fm.eventclasses",
        "json_depends_on": ["fm.alarmclasses"],
        "json_unique_fields": ["name"],
    }
    name = StringField(required=True, unique=True)
    uuid = UUIDField(binary=True)
    description = StringField(required=False)
    # Event processing action:
    #     D - Drop
    #     L - Log as processed, do not move to archive
    #     A - Log as processed, move to archive
    action = StringField(
        required=True, choices=[("D", "Drop"), ("L", "Log"), ("A", "Log & Archive")]
    )
    vars = ListField(EmbeddedDocumentField(EventClassVar))
    # Text messages
    subject_template = StringField()
    body_template = StringField()
    symptoms = StringField()
    probable_causes = StringField()
    recommended_actions = StringField()

    disposition = ListField(EmbeddedDocumentField(EventDispositionRule))
    repeat_suppression = ListField(EmbeddedDocumentField(EventSuppressionRule))
    # Window to suppress duplicated events (in seconds)
    # 0 means no deduplication
    deduplication_window = IntField(default=3)
    # Time to live in active window, unless not belonging to any alarm
    # (in seconds)
    ttl = IntField(default=86400)
    # True if event processing is regulated by
    # Interface Profile.link_events setting
    link_event = BooleanField(default=False)
    #
    handlers = ListField(StringField())
    # Plugin settings
    plugins = ListField(EmbeddedDocumentField(EventPlugin))
    #
    category = ObjectIdField()

    _id_cache = cachetools.TTLCache(maxsize=100, ttl=60)
    _name_cache = cachetools.TTLCache(maxsize=100, ttl=60)
    _handlers_cache = {}

    def __str__(self):
        return self.name

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_by_id(cls, id):
        return EventClass.objects.filter(id=id).first()

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_by_name(cls, name):
        return EventClass.objects.filter(name=name).first()

    def get_handlers(self):
        @cachetools.cached(self._handlers_cache, key=lambda x: x.id, lock=handlers_lock)
        def _get_handlers(event_class):
            handlers = []
            for hh in event_class.handlers:
                try:
                    h = get_handler(hh)
                except ImportError:
                    h = None
                if h:
                    handlers += [h]
            return handlers

        return _get_handlers(self)

    def save(self, *args, **kwargs):
        c_name = " | ".join(self.name.split(" | ")[:-1])
        c = EventClassCategory.objects.filter(name=c_name).first()
        if not c:
            c = EventClassCategory(name=c_name)
            c.save()
        self.category = c.id
        super(EventClass, self).save(*args, **kwargs)

    @property
    def display_action(self):
        return {"D": "Drop", "L": "Log", "A": "Log and Archive"}[self.action]

    def to_json(self):
        c = self
        r = ["{"]
        r += ['    "name": "%s",' % q(c.name)]
        r += ['    "$collection": "%s",' % self._meta["json_collection"]]
        r += ['    "uuid": "%s",' % c.uuid]
        if c.description:
            r += ['    "description": "%s",' % q(c.description)]
        r += ['    "action": "%s",' % q(c.action)]
        # vars
        vars = []
        for v in c.vars:
            vd = ["        {"]
            vd += ['            "name": "%s",' % q(v.name)]
            vd += ['            "description": "%s",' % q(v.description)]
            vd += ['            "type": "%s",' % q(v.type)]
            vd += ['            "required": %s' % q(v.required)]
            vd += ["        }"]
            vars += ["\n".join(vd)]
        r += ['    "vars": [']
        r += [",\n".join(vars)]
        r += ["    ],"]
        if self.link_event:
            r += ['    "link_event": true,']
        r += ['    "deduplication_window": %d,' % self.deduplication_window]
        r += ['    "ttl": %d,' % self.ttl]
        # Handlers
        if self.handlers:
            hh = ['        "%s"' % h for h in self.handlers]
            r += ['    "handlers": [']
            r += [",\n\n".join(hh)]
            r += ["    ],"]
        # Text
        r += ['    "subject_template": "%s",' % q(c.subject_template)]
        r += ['    "body_template": "%s",' % q(c.body_template)]
        r += ['    "symptoms": "%s",' % q(c.symptoms)]
        r += ['    "probable_causes": "%s",' % q(c.probable_causes)]
        r += ['    "recommended_actions": "%s",' % q(c.recommended_actions)]
        # Disposition rules
        if c.disposition:
            r += ['    "disposition": [']
            disp = []
            for d in c.disposition:
                ll = ["        {"]
                lll = ['            "name": "%s"' % q(d.name)]
                lll += ['            "condition": "%s"' % q(d.condition)]
                lll += ['            "action": "%s"' % q(d.action)]
                if d.alarm_class:
                    lll += ['            "alarm_class__name": "%s"' % q(d.alarm_class.name)]
                if d.managed_object:
                    lll += ['            "managed_object": "%s"' % q(d.managed_object)]
                ll += [",\n".join(lll)]
                ll += ["        }"]
                disp += ["\n".join(ll)]
            r += [",\n".join(disp)]
            r += ["    ]"]
            #
            if not r[-1].endswith(","):
                r[-1] += ","
        r += ['    "repeat_suppression": [']
        if c.repeat_suppression:
            rep = []
            for rs in c.repeat_suppression:
                ll = ["        {"]
                lll = ['            "name": "%s",' % q(rs.name)]
                lll += ['            "condition": "%s",' % q(rs.condition)]
                lll += ['            "event_class__name": "%s",' % q(rs.event_class.name)]
                lll += ['            "match_condition": {']
                llll = []
                for rsc in rs.match_condition:
                    llll += ['                "%s": "%s"' % (q(rsc), q(rs.match_condition[rsc]))]
                lll += [",\n".join(llll) + "\n            },"]
                lll += ['            "window": %d,' % rs.window]
                lll += ['            "suppress": %s' % ("true" if rs.suppress else "false")]
                ll += ["\n".join(lll)]
                ll += ["        }"]
                rep += ["\n".join(ll)]
            r += [",\n".join(rep)]
        r += ["    ]"]
        # Plugins
        if self.plugins:
            if not r[-1].endswith(","):
                r[-1] += ","
            plugins = []
            for p in self.plugins:
                pd = ["        {"]
                pd += ['            "name": "%s"' % p.name]
                if p.config:
                    pd[-1] += ","
                    pc = []
                    for v in p.config:
                        pc += ['                "%s": "%s"' % (v, p.config.vars[v])]
                    pd += ['            "config": {']
                    pd += [",\n".join(pc)]
                    pd += ["            }"]
                pd += ["        }"]
                plugins += ["\n".join(pd)]
            r += ['    "plugins": [']
            r += [",\n".join(plugins)]
            r += ["    ]"]
        # Close
        if r[-1].endswith(","):
            r[-1] = r[-1][:-1]
        r += ["}", ""]
        return "\n".join(r)

    def get_json_path(self):
        p = [quote_safe_path(n.strip()) for n in self.name.split("|")]
        return os.path.join(*p) + ".json"


rx_rule_name_quote = re.compile("[^a-zA-Z0-9]+")


def rulename_quote(s):
    """
    Convert arbitrary string to pyrule name

    >>> rulename_quote("Unknown | Default")
    'Unknown_Default'
    """
    return rx_rule_name_quote.sub("_", s)
