# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# cm.reportvalidationmethods
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.lib.app.simplereport import SimpleReport, SectionRow
from noc.cm.validators.base import validator_registry
from noc.core.translation import ugettext as _


class ReportvalidationmethodsApplication(SimpleReport):
    title = _("Validation Methods")

    def get_data(self, **kwargs):
        ov = {}
        iv = {}
        for vn in validator_registry.validators:
            v = validator_registry.validators[vn]
            scopes = []
            if v.is_object():
                scopes += ["OBJECT"]
            if v.is_interface():
                scopes += ["INTERFACE"]
            r = [
                SectionRow("[%s] %s" % (", ".join(scopes), v.TITLE)),
                [_("Description"), v.DESCRIPTION],
                [_("Handler"), "%s.%s" % (v.__module__, v.__name__)],
                [_("Tags"), ", ".join(v.TAGS or [])],
            ]
            if v.is_object():
                ov[v.TITLE] = r
            if v.is_interface():
                iv[v.TITLE] = r
        r = []
        for vn in sorted(ov):
            r += ov[vn]
        for vn in sorted(iv):
            r += iv[vn]
        return self.from_dataset(title=self.title, columns=["", ""], data=r)
