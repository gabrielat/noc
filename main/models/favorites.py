# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Favorites model
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import logging

# Third-party modules
from mongoengine.document import Document
from mongoengine.fields import StringField, ListField, BooleanField
import six

# NOC modules
from noc.core.mongo.fields import ForeignKeyField
from noc.aaa.models.user import User

logger = logging.getLogger(__name__)


@six.python_2_unicode_compatible
class Favorites(Document):
    meta = {
        "collection": "noc.favorites",
        "strict": False,
        "auto_create_index": False,
        "indexes": ["user", ("user", "app")],
    }

    user = ForeignKeyField(User)
    app = StringField()
    favorite_app = BooleanField(default=False)
    favorites = ListField()

    def __unicode__(self):
        return "%s:%s" % (self.user.username, self.app)

    @classmethod
    def add_item(cls, user, app_id, item):
        fv = Favorites.objects.filter(user=user.id, app=app_id).first()
        if not fv:
            fv = Favorites(user=user.id, app=app_id, favorites=[])
        fi = list(fv.favorites) or []
        if item not in fi:
            logger.info("Setting favorite item %s@%s for user %s", item, app_id, user.username)
            fv.favorites = fi + [item]
            fv.save()

    @classmethod
    def remove_item(cls, user, app_id, item):
        fv = Favorites.objects.filter(user=user.id, app=app_id).first()
        fi = list(fv.favorites) or []
        if fv and item and item in fi:
            logger.info("Resetting favorite item %s@%s for user %s", item, app_id, user.username)
            fi.remove(item)
            fv.favorites = fi
            fv.save()
