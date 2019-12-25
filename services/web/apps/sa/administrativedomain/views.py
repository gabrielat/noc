# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# sa.administrativedomain application
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.lib.app.extmodelapplication import ExtModelApplication, view
from noc.sa.models.administrativedomain import AdministrativeDomain
from noc.core.comp import smart_text
from noc.core.translation import ugettext as _


class AdministrativeDomainApplication(ExtModelApplication):
    """
    AdministrativeDomain application
    """

    title = _("Administrative Domains")
    menu = [_("Setup"), _("Administrative Domains")]
    model = AdministrativeDomain
    protected_fields = {"remote_system", "remote_id"}
    query_fields = ["name__icontains", "description__icontains"]
    lookup_default = [{"has_children": False, "id": "Leave unchanged", "label": "Leave unchanged"}]

    def field_object_count(self, o):
        return o.managedobject_set.count()

    def instance_to_lookup(self, o, fields=None):
        return {"id": o.id, "label": smart_text(o), "has_children": o.has_children}

    @view(r"^(?P<id>\d+)/get_path/$", access="read", api=True)
    def api_get_path(self, request, id):
        o = self.get_object_or_404(AdministrativeDomain, id=id)
        path = [AdministrativeDomain.objects.get(id=ns) for ns in o.get_path()]
        return {
            "data": [
                {"level": path.index(p) + 1, "id": str(p.id), "label": smart_text(p.name)}
                for p in path
            ]
        }
