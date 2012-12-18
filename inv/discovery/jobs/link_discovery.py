## -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Link Discovery Abstract Job
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import datetime
from collections import defaultdict
## NOC modules
from base import MODiscoveryJob
from noc.settings import config
from noc.inv.models.pendinglinkcheck import PendingLinkCheck
from noc.inv.models.interface import Interface


class LinkDiscoveryJob(MODiscoveryJob):
    """
    Abstract class for link discovery jobs
    """
    name = None
    map_task = None
    method = None
#    ignored = not config.getboolean("interface_discovery", "enabled")
#    initial_submit_interval = config.getint("interface_discovery",
#        "initial_submit_interval")
#    initial_submit_concurrency = config.getint("interface_discovery",
#        "initial_submit_concurrency")

    def submit_candidate(self, local_interface,
                         remote_object, remote_interface=None):
        """
        Submit link candidate
        :param local_interface:
        :param remote_object:
        :param remote_interface:
        :return:
        """
        self.debug("Link candidate found: %s -> %s:%s" % (
            local_interface, remote_object.name, remote_interface))
        self.candidates[remote_object] += [
            (local_interface, remote_interface)
        ]

    def submit_link(self, local_object, local_interface,
                    remote_object, remote_interface):
        l_iface = Interface.objects.filter(
            managed_object=local_object.id,
            name=local_interface).first()
        if not l_iface:
            self.error("Interface is not found: %s:%s" % (
                local_object.name, local_interface))
            return
        r_iface = Interface.objects.filter(
            managed_object=remote_object.id,
            name=remote_interface).first()
        if not r_iface:
            self.error("Interface is not found: %s:%s" % (
                remote_object.name, remote_interface))
            return
        # @todo: LAG
        link = l_iface.link
        if link:
            if link.other(l_iface) != r_iface:
                self.error("Found link %s - %s conflicts with existing %s" % (
                    l_iface, r_iface, link))
        else:
            self.debug("Linking %s and %s" % (l_iface, r_iface))
            l_iface.link_ptp(r_iface)
            self.submited.add((local_interface, remote_object, remote_interface))

    def process_result(self, object, result):
        """
        Process job result and submit candidates
        :param result:
        :return:
        """
        raise NotImplementedError()

    def handler(self, object, result):
        """
        :param object:
        :param result:
        :return:
        """
        # Process results
        self.submited = set()
        self.candidates = defaultdict(list)  # remote -> [(local iface, remote_iface)]
                                             # remote iface may be unknown
        self.process_result(object, result)
        # Process pending link checks
        self.p_candidates = defaultdict(list)  # remote -> [(local iface, remote_iface)]
                                               # local iface may be unknown
        for plc in PendingLinkCheck.objects.filter(
            method=self.method, local_object=object.id,
            expire__gt=datetime.datetime.now()):
            if plc.local_object not in self.candidates:
                continue
            self.p_candidates[plc.remote_object] += [(plc.local_interface, plc.remote_interface)]
        # Resolve self links
        if object in self.candidates:
            sl = set()
            for l, r in self.candidates[object]:
                if (l and r and l != r and (l, r) not in sl
                    and (r, l) not in sl):
                    sl.add((l, r))
            for l, r in sl:
                self.submit_link(object, l, object, r)
        # Process pending checks
        for pr in self.p_candidates:
            # Check remote object in pending checks
            if pr not in self.candidates:
                continue
            pc = self.p_candidates
            c = self.candidates[pr]
            if len(pc) == 1 and len(c) == 1:
                # 1:1 link
                pcl, pcr = pc[0]
                cl, cr = c[0]
                if ((pcl is None or cl is None or pcl == cl) and
                    (pcr is None or cr is None or pcr == cr)):
                    self.submit_link(object, cl, pr, pcr)
            else:
                # N:N link
                # Join pending and found results
                # @todo
                pass
        # Clean my pending link checks
        PendingLinkCheck.objects.filter(
            method=self.method, local_object=object.id).delete()
        # Write pending checks
        for o in self.candidates:
            for l, r in self.candidates[o]:
                if (l, o, r) not in self.submited:
                    self.debug("Scheduling check for %s:%s -> %s:%s" % (object.name, l, o, r))
                    PendingLinkCheck.submit(self.method, o, r, object, l)
        # Reschedule pending jobs
        # @todo: Reschedule only if no pending checks has been processed
        self.debug("Rescheduling: %r" % set(self.candidates))
        return True

    @classmethod
    def initial_submit_queryset(cls):
        return {"object_profile__enable_%s_discovery" % cls.method: True}

    def can_run(self):
        return (super(LinkDiscoveryJob, self).can_run()
                and getattr(self.object.object_profile,
                    "enable_%s_discovery" % self.method))

    @classmethod
    def get_submit_interval(cls, object):
        return getattr(object.object_profile,
            "%s_discovery_max_interval" % cls.method)

    def get_failed_interval(self):
        return getattr(self.object.object_profile,
            "%s_discovery_min_interval" % self.method)
