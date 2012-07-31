# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## AdministrativeDomain
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Django modules
from django.utils.translation import ugettext_lazy as _
from django.db import models


class AdministrativeDomain(models.Model):
    """
    Administrative Domain
    """
    class Meta:
        verbose_name = _("Administrative Domain")
        verbose_name_plural = _("Administrative Domains")
        db_table = "sa_administrativedomain"
        app_label = "sa"
        ordering = ["name"]

    name = models.CharField(_("Name"), max_length=32, unique=True)
    description = models.TextField(
        _("Description"),
        null=True, blank=True)

    def __unicode__(self):
        return self.name
