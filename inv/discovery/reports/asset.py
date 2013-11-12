## -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Asset Discovery Report
##----------------------------------------------------------------------
## Copyright (C) 2007-2013 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from collections import defaultdict
## Third-party modules
from mongoengine.queryset import Q
## NOC modules
from base import Report
from noc.inv.models.objectmodel import ObjectModel
from noc.inv.models.object import Object
from noc.inv.models.vendor import Vendor
from noc.inv.models.connectionrule import ConnectionRule
from noc.inv.models.error import ConnectionError
from noc.lib.text import str_dict
from noc.inv.models.error import ConnectionError


class AssetReport(Report):
    system_notification = "inv.asset_discovery"

    def __init__(self, job, enabled=True, to_save=False):
        super(AssetReport, self).__init__(
            job, enabled=enabled, to_save=to_save)
        self.om_cache = {}  # part_no -> object model
        self.unknown_part_no = {}  # part_no -> list of variants
        self.pn_description = {}  # part_no -> Description
        self.vendors = {}  # code -> Vendor instance
        self.objects = []  # [(type, object, context)]
        self.rule = defaultdict(list)  # Connection rule. type -> [rule1, ruleN]
        self.rule_context = {}
        self.ctx = {}

    def submit(self, type, part_no, number=None,
               builtin=False,
               vendor=None,
               revision=None, serial=None,
               description=None):
        # Set contexts
        self.set_context("N", number)
        if type in self.rule_context:
            scope, reset_scopes = self.rule_context[type]
            if scope:
                self.set_context(scope, number)
            if reset_scopes:
                self.reset_context(reset_scopes)
        # Skip builtin modules
        if builtin:
            return
        # Cache description
        if description:
            for p in part_no:
                if p not in self.pn_description:
                    self.pn_description[p] = description
        # Find vendor
        vnd = self.get_vendor(vendor)
        if not vnd:
            self.error("Unknown vendor '%s' for S/N %s (%s)" % (
                vendor, serial, description))
            return
        # Find model
        m = self.get_model(vnd, part_no)
        if not m:
            self.debug("Unknown model: vendor=%s, part_no=%s (%s). Skipping" % (
                vnd.name, description, part_no))
            self.register_unknown_part_no(part_no)
            return
        # Get connection rule
        if not self.rule and m.connection_rule:
            self.set_rule(m.connection_rule)
            # Set initial context
            if type in self.rule_context:
                scope = self.rule_context[type][0]
                if scope:
                    self.set_context(scope, number)
        # Find existing object or create new
        o = Object.objects.filter(
            model=m.id, data__asset__serial=serial).first()
        if not o:
            # Create new object
            self.info("Creating new object. model='%s', serial='%s'" % (
                m.name, serial))
            o = Object(model=m, data={"asset": {"serial": serial}})
            o.save()
        # Check revision
        if o.get_data("asset", "revision") != revision:
            # Update revision
            self.info("Object revision changed [%s %s] %s -> %s" % (
                m.name, o.id, o.get_data("asset", "revision"), revision
            ))
            o.set_data("asset", "revision", revision)
            o.save()
        # Check management
        if o.get_data("management", "managed"):
            if o.get_data("management", "managed_object") != self.object.id:
                self.info("Changing object management to '%s'" % self.object.name)
                o.set_data("management", "managed_object", self.object.id)
                o.save()
        self.objects += [(type, o, self.ctx.copy())]

    def iter_object(self, i, scope, value, target_type, fwd):
        # Search backwards
        if not fwd:
            for j in range(i - 1, -1, -1):
                type, object, ctx = self.objects[j]
                if scope in ctx and ctx[scope] == value:
                    if target_type == type:
                        yield type, object, ctx
                else:
                    break
        # Search forward
        if fwd:
            for j in range(i + 1, len(self.objects)):
                type, object, ctx = self.objects[j]
                if scope in ctx and ctx[scope] == value:
                    if target_type == type:
                        yield type, object, ctx
                else:
                    raise StopIteration

    def expand_context(self, s, ctx):
        """
        Replace values in context
        """
        for c in ctx:
            s = s.replace("{%s}" % c, str(ctx[c]))
        return s

    def submit_connections(self):
        # Check connection rule is set
        if not self.rule:
            return
        for i, o in enumerate(self.objects):
            type, object, context = o
            self.debug("Trying to connect #%d. %s (%s)" % (
                i, type, str_dict(context)))
            if type not in self.rule:
                continue
            # Find applicable rule
            for r in self.rule[type]:
                found = False
                t_n = self.expand_context(r.target_number, context)
                if r.scope.startswith("-"):
                    scope = r.scope[1:]
                    fwd = True
                else:
                    scope = r.scope
                    fwd = False
                for t_type, t_object, t_ctx in self.iter_object(
                        i, scope, context.get(scope), r.target_type, fwd=fwd):
                    if not t_n or t_n == t_ctx["N"]:
                        # Match
                        m_c = self.expand_context(r.match_connection, context)
                        t_c = self.expand_context(r.target_connection, context)
                        self.info("Connecting %s %s:%s -> %s %s:%s" % (
                            type, context["N"], m_c,
                            t_type, t_ctx["N"], t_c
                        ))
                        try:
                            object.connect_p2p(m_c, t_object, t_c, {},
                                               reconnect=True)
                        except ConnectionError, why:
                            self.error("Failed to connect: %s" % why)
                        found = True
                        break
                if found:
                    break

    def send(self):
        if self.unknown_part_no:
            platform = self.object.platform
            upn = self.get_unknown_part_no()
            for pns in upn:
                # Find description
                description = "no description"
                for p in pns:
                    if p in self.pn_description:
                        description = self.pn_description[p]
                        break
                # Report error
                self.error("Unknown part number for %s: %s (%s)" % (
                    platform, ", ".join(pns), description))

    def get_model(self, vendor, part_no):
        """
        Get ObjectModel by part part_no,
        Search order:
            * NOC model name
            * asset.part_no* value (Part numbers)
            * asset.order_part_no* value (FRU numbers)
        """
        # Process list of part no
        if type(part_no) == list:
            for p in part_no:
                m = self.get_model(vendor, p)
                if m:
                    return m
            return None
        # Process scalar type
        m = self.om_cache.get(part_no)
        if m:
            return m
        # Check for model name
        if " | " in part_no:
            m = ObjectModel.objects.filter(name=part_no).first()
            if m:
                self.om_cache[part_no] = m
                return m
        vq = Q(vendor=vendor.id)
        # Check for asset.part_no*
        q = vq & (
            Q(data__asset__part_no0=part_no) |
            Q(data__asset__part_no1=part_no) |
            Q(data__asset__part_no2=part_no) |
            Q(data__asset__part_no3=part_no)
        )
        m = ObjectModel.objects.filter(q).first()
        if m:
            self.om_cache[part_no] = m
            return m
        # Check for asset.order_part_no*
        q = vq & (
            Q(data__asset__order_part_no0=part_no) |
            Q(data__asset__order_part_no1=part_no) |
            Q(data__asset__order_part_no2=part_no) |
            Q(data__asset__order_part_no3=part_no)
        )
        m = ObjectModel.objects.filter(q).first()
        if m:
            self.om_cache[part_no] = m
            return m
        # Not found
        self.om_cache[part_no] = None
        return None

    def register_unknown_part_no(self, part_no):
        """
        Register missed part number
        """
        if type(part_no) != list:
            part_no = [part_no]
        for p in part_no:
            if p not in self.unknown_part_no:
                self.unknown_part_no[p] = set()
            for pp in part_no:
                self.unknown_part_no[p].add(pp)

    def get_unknown_part_no(self):
        """
        Get list of missed part number variants
        """
        r = []
        for p in self.unknown_part_no:
            n = sorted(self.unknown_part_no[p])
            if n not in r:
                r += [n]
        return r

    def get_vendor(self, v):
        """
        Get vendor instance or None
        """
        if v is None:
            v = "NONAME"
        v = v.upper()
        if v in self.vendors:
            return self.vendors[v]
        o = Vendor.objects.filter(code=v).first()
        if o:
            self.vendors[v] = o
            return o
        else:
            self.vendors[v] = None
            return None

    def set_rule(self, rule):
        self.debug("Setting connection rule '%s'" % rule.name)
        # Compile context mappings
        self.rule_context = {}
        for ctx in rule.context:
            self.rule_context[ctx.type] = (ctx.scope, ctx.reset_scopes)
        self.debug("Context mappings: %s" % self.rule_context)
        # Compile rules
        for r in rule.rules:
            self.rule[r.match_type] += [r]

    def set_context(self, name, value):
        self.ctx[name] = value
        n = "N%s" % name
        if n not in self.ctx:
            self.ctx[n] = 0
        else:
            self.ctx[n] += 1
        self.debug("Set context %s = %s -> %s" % (
            name, value, str_dict(self.ctx)))

    def reset_context(self, names):
        for n in names:
            if n in self.ctx:
                del self.ctx[n]
            m = "N%s" % n
            if m in self.ctx:
                del self.ctx[m]
        self.debug("Reset context scopes %s -> %s" % (
            ", ".join(names), str_dict(self.ctx)))
