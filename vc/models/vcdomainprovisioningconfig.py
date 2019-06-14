# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# VCDomainProvisioningConfig
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
from noc.sa.models.managedobjectselector import ManagedObjectSelector
from noc.main.models.notificationgroup import NotificationGroup
from .vcdomain import VCDomain
from .vcfilter import VCFilter


@tuck_up_pants
@six.python_2_unicode_compatible
class VCDomainProvisioningConfig(models.Model):
    """
    VCDomain Provisioning Parameters
    """
    class Meta(object):
        verbose_name = "VC Domain Provisioning Config"
        verbose_name_plural = "VC Domain Provisioning Config"
        db_table = "vc_vcdomainprovisioningconfig"
        app_label = "vc"
        unique_together = [("vc_domain", "selector")]

    vc_domain = models.ForeignKey(VCDomain, verbose_name="VC Domain")
    selector = models.ForeignKey(ManagedObjectSelector,
                                 verbose_name="Managed Object Selector")
    is_enabled = models.BooleanField("Is Enabled", default=True)
    vc_filter = models.ForeignKey(VCFilter, verbose_name="VC Filter",
                                  null=True, blank=True)
    tagged_ports = models.CharField("Tagged Ports", max_length=256, null=True,
                                    blank=True)
    notification_group = models.ForeignKey(NotificationGroup,
                                           verbose_name="Notification Group",
                                           null=True, blank=True)

    def __str__(self):
        return u"%s: %s" % (unicode(self.vc_domain), unicode(self.selector))

    @property
    def tagged_ports_list(self):
        """
        Returns a list of tagged ports
        """
        if self.tagged_ports:
            return [x.strip() for x in self.tagged_ports.split(",")]
        else:
            return []
