# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# RefBookData
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
# Third-party modules
import six
from django.db import models
# NOC modules
from noc.core.model.hacks import tuck_up_pants
from noc.core.model.fields import TextArrayField
from .refbook import RefBook


class RBDManader(models.Manager):
    """
    Ref Book Data Manager
    """
    # Order by first field
    def get_queryset(self):
        return super(RBDManader, self).get_queryset().extra(order_by=["main_refbookdata.value[1]"])


@tuck_up_pants
@six.python_2_unicode_compatible
class RefBookData(models.Model):
    """
    Ref. Book Data
    """
    class Meta(object):
        app_label = "main"
        verbose_name = "Ref Book Data"
        verbose_name_plural = "Ref Book Data"

    ref_book = models.ForeignKey(RefBook, verbose_name="Ref Book")
    value = TextArrayField("Value")

    objects = RBDManader()

    def __str__(self):
        return u"%s: %s" % (self.ref_book, self.value)

    @property
    def items(self):
        """
        Returns list of pairs (field,data)
        """
        return zip(self.ref_book.fields, self.value)
