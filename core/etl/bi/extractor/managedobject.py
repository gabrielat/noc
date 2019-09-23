# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Managed Object Extractor
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
import datetime
from collections import defaultdict

# NOC modules
from .base import BaseExtractor
from noc.core.text import ch_escape
from noc.sa.models.managedobject import ManagedObject, ManagedObjectAttribute
from noc.bi.models.managedobjects import ManagedObject as ManagedObjectBI
from noc.core.etl.bi.stream import Stream
from noc.inv.models.interface import Interface
from noc.inv.models.link import Link
from noc.inv.models.capability import Capability
from noc.sa.models.objectcapabilities import ObjectCapabilities
from noc.inv.models.discoveryid import DiscoveryID
from noc.fm.models.uptime import Uptime


class ManagedObjectsExtractor(BaseExtractor):
    name = "managedobjects"
    is_snapshot = True

    # Caps to field mapping
    CAPS_MAP = {
        "Network | STP": "has_stp",
        "Network | CDP": "has_cdp",
        "Network | LLDP": "has_lldp",
        "SNMP": "has_snmp",
        "SNMP | v1": "has_snmp_v1",
        "SNMP | v2c": "has_snmp_v2c",
    }

    def __init__(self, prefix, start, stop):
        super(ManagedObjectsExtractor, self).__init__(prefix, start, stop)
        self.mo_stream = Stream(ManagedObjectBI, prefix)

    def extract(self):
        nr = 0
        ts = datetime.datetime.now()
        # External data
        x_data = [self.get_interfaces(), self.get_links(), self.get_caps()]
        sn = self.get_mo_sn()
        # Extract managed objects
        for mo in ManagedObject.objects.all().iterator():
            did = DiscoveryID.objects.filter(object=mo).first()
            uptime = Uptime.objects.filter(object=mo.id, stop=None).first()
            serials = sn.get(mo.id, [])
            inventory = mo.get_inventory()
            if inventory:
                serials += inventory[0].get_object_serials(chassis_only=False)
            location = ""
            if mo.container:
                location = mo.container.get_address_text()
            r = {
                "ts": ts,
                "managed_object": mo,
                "profile": mo.profile,
                "administrative_domain": mo.administrative_domain,
                "segment": mo.segment,
                "container": mo.container,
                "level": mo.object_profile.level,
                "x": mo.x,
                "y": mo.y,
                "pool": mo.pool,
                # "object_profile": mo.object_profile,
                "vendor": mo.vendor,
                "platform": mo.platform,
                "hw_version": mo.get_attr("HW version", default=None),
                "version": mo.version,
                "bootprom_version": mo.get_attr("Boot PROM", default=None),
                "name": ch_escape(mo.name),
                "hostname": ch_escape(did.hostname or "") if did else "",
                "ip": mo.address,
                "is_managed": mo.is_managed,
                "location": ch_escape(location) if location else "",
                "uptime": uptime.last_value if uptime else 0.0,
                "tags": [str(t) for t in mo.tags if "{" not in t] if mo.tags else [],  # { - bug
                "serials": list(set(serials))
                # subscribers
                # services
            }
            # Apply external data
            for data in x_data:
                d = data.get(mo.id)
                if d:
                    r.update(d)
            # Submit
            self.mo_stream.push(**r)
            nr += 1
        self.mo_stream.finish()
        return nr

    def get_links(self):
        """
        Build discovery method summary
        :return:
        """
        t = defaultdict(int)  # object -> count
        r = defaultdict(int)  # object_id, method -> count
        neighbors = defaultdict(set)  # object_id -> {objects}
        for d in Link._get_collection().find():
            method = d.get("discovery_method")
            linked = d.get("linked_objects", [])
            for o in linked:
                r[o, method] += 1
                t[o] += 1
                neighbors[o].update(linked)
        return dict(
            (
                o,
                {
                    "n_neighbors": len(neighbors[o]),
                    "n_links": t[o],
                    "nri_links": r[o, "nri"],
                    "mac_links": r[o, "mac"],
                    "stp_links": r[o, "stp"],
                    "lldp_links": r[o, "lldp"],
                    "cdp_links": r[o, "cdp"],
                },
            )
            for o in t
        )

    def get_interfaces(self):
        """
        Build interface counts
        :return:
        """
        r = Interface._get_collection().aggregate(
            [
                {"$match": {"type": "physical"}},
                {"$group": {"_id": "$managed_object", "total": {"$sum": 1}}},
            ]
        )
        return dict((d["_id"], {"n_interfaces": d["total"]}) for d in r)

    def get_caps(self):
        # name -> id map
        caps = dict(
            (self.CAPS_MAP[d["name"]], d["_id"])
            for d in Capability._get_collection().find(
                {"name": {"$in": list(self.CAPS_MAP)}}, {"_id": 1, "name": 1}
            )
        )
        # object -> caps
        add_expr = dict((c, {"$in": [caps[c], "$caps.capability"]}) for c in caps)
        project_expr = dict((c, 1) for c in caps)
        project_expr["_id"] = 1
        return dict(
            (d["_id"], dict((x, d[x]) for x in d if x != "_id"))
            for d in ObjectCapabilities._get_collection().aggregate(
                [{"$addFields": add_expr}, {"$project": project_expr}]
            )
        )

    @staticmethod
    def get_mo_sn():
        """
        Extract serial number from attributes
        :return:
        """
        r = {
            mo_id: [serial]
            for mo_id, serial in ManagedObjectAttribute.objects.filter(
                key="Serial Number"
            ).values_list("managed_object", "value")
        }
        return r
