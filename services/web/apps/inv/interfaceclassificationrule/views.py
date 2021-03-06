# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# inv.interfaceclassificationrule application
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.lib.app.extdocapplication import ExtDocApplication
from noc.inv.models.interfaceclassificationrule import InterfaceClassificationRule
from noc.core.translation import ugettext as _


class InterfaceClassificationRuleApplication(ExtDocApplication):
    """
    InterfaceClassificationRule application
    """

    title = _("Interface Classification Rule")
    menu = [_("Setup"), _("Interface Classification Rules")]
    model = InterfaceClassificationRule

    query_fields = ["name__icontains", "description__icontains"]
    default_ordering = ["order"]

    def field_row_class(self, o):
        if o.profile and o.profile.style:
            return o.profile.style.css_class_name
        else:
            return ""

    def field_match_expr(self, o):
        return o.match_expr
