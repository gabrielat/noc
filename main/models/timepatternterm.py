# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# TimePatternTerm database model
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
from noc.lib.timepattern import TimePattern as TP
from .timepattern import TimePattern


@tuck_up_pants
@six.python_2_unicode_compatible
class TimePatternTerm(models.Model):
    """
    Time pattern terms
    """
    class Meta(object):
        verbose_name = "Time Pattern Term"
        verbose_name_plural = "Time Pattern Terms"
        db_table = "main_timepatternterm"
        app_label = "main"
        unique_together = [("time_pattern", "term")]

    time_pattern = models.ForeignKey(TimePattern,
                                     verbose_name="Time Pattern")
    term = models.CharField("Term", max_length=256)

    def __str__(self):
        return u"%s: %s" % (self.time_pattern.name, self.term)

    @classmethod
    def check_syntax(cls, term):
        """
        Checks Time Pattern syntax. Raises SyntaxError in case of error
        """
        TP(term)

    def save(self, *args):
        """
        Check syntax before save
        """
        TimePatternTerm.check_syntax(self.term)
        super(TimePatternTerm, self).save(*args)
