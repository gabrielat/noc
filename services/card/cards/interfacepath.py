# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# interfacepath card
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
import datetime

#  Third-party modules
from typing import Dict, Any, List, Tuple, Set
import ujson

# NOC modules
from noc.config import config
from noc.sa.models.managedobject import ManagedObject
from noc.inv.models.interface import Interface
from noc.core.topology.path import KSPFinder
from noc.core.topology.goal.level import ManagedObjectLevelGoal
from noc.core.text import split_alnum
from noc.core.bi.decorator import bi_hash
from noc.core.clickhouse.connect import connection as ch_connection
from noc.core.clickhouse.error import ClickhouseError
from noc.core.hash import hash_str
from .base import BaseCard


class InterfacePathCard(BaseCard):
    name = "interfacepath"
    default_template_name = "interfacepath"
    model = Interface
    N_PATHS = 2
    SIG_LEN = 9  # odd padding to broke base64

    def get_data(self):
        # type: () -> Dict[str, Any]
        r = {
            "object": self.object,
            "paths": [],
            "link_sets": 0,
            "if_hash": {},
            "error": None,
            "ajax_query_key": None,
        }  # type: Dict[str, Any]
        mo = self.object.managed_object
        target_level = (mo.object_profile.level // 10 + 1) * 10
        try:
            finder = KSPFinder(mo, ManagedObjectLevelGoal(target_level), n_shortest=self.N_PATHS)
            for path in finder.iter_shortest_paths():
                items = []  # type: List[Dict[str, Any]]
                ingress_links = [[self.object]]  # type: List[List[Interface]]
                for pi in path:
                    item = {
                        "object": pi.start,
                        "ingress": ingress_links,
                        "egress": [],
                    }  # type: Dict[str, Any]
                    ingress_links = []
                    for link in pi.links:
                        egress, ingress = self.split_interfaces(pi.start, link.interfaces)
                        ingress_links += [ingress]
                        item["egress"] += [egress]
                    r["link_sets"] = max(r["link_sets"], len(item["egress"]))
                    items += [item]
                items += [{"object": pi.end, "ingress": ingress_links, "egress": []}]
                r["paths"] += [items]
        except ValueError as e:
            r["error"] = str(e)
            return r
        # Build interface hashes
        to_collect = set()  # type: Set[Tuple[int, str]]
        for path in r["paths"]:
            for item in path:
                for direction in ("ingress", "egress"):
                    for link in item[direction]:
                        for iface in link:
                            ifname = iface.name
                            if ifname not in r["if_hash"]:
                                r["if_hash"][ifname] = bi_hash(ifname)
                            to_collect.add((iface.managed_object.bi_id, ifname))
        # @todo: Encrypt
        r["ajax_query_key"] = self.encode_query(to_collect)
        return r

    @classmethod
    def get_signature(cls, data):
        # (str) -> str
        """
        Get tamper-protection signature

        :param data: Input data
        :return: Tamper-protection signature
        """
        return hash_str(config.secret_key + data).encode("base64")[: cls.SIG_LEN]

    @classmethod
    def encode_query(cls, to_collect):
        # type: (Set[Tuple[int, str]]) -> str
        data = ujson.dumps(to_collect).encode("base64").replace("\n", "")
        return cls.get_signature(data) + data

    @classmethod
    def decode_query(cls, query):
        # type: (str) -> List[Tuple[int, str]]
        sig, data = query[: cls.SIG_LEN], query[cls.SIG_LEN :]
        if sig != cls.get_signature(data):
            raise ValueError
        return ujson.loads(data.decode("base64"))

    @staticmethod
    def split_interfaces(obj, interfaces):
        # type: (ManagedObject, List[Interface]) -> Tuple[List[Interface], List[Interface]]
        """
        Split list of interfaces of the links to egress (belonging to `obj`)
        and ingress (leading out of object)
        :param obj: Managed Object
        :param interfaces:  List of link interfaces
        :return: List of egress links, List of ingress links
        """
        ingress = []  # type: List[Interface]
        egress = []  # type: List[Interface]
        for iface in sorted(interfaces, key=lambda x: split_alnum(x.name)):
            if iface.managed_object == obj:
                egress += [iface]
            else:
                ingress += [iface]
        return egress, ingress

    @staticmethod
    def humanize_metric(value):
        # type: (str) -> str
        if not value:
            return "-"
        cv = float(value)
        for t, n in [(1000000000, "G"), (1000000, "M"), (1000, "k")]:
            if cv >= t:
                if cv // t * t == cv:
                    return "%d%s" % (cv // t, n)
                else:
                    return "%.2f%s" % (float(cv) / t, n)
        return str(cv)

    def get_ajax_data(self, **kwargs):
        # Parse query params
        query = self.decode_query(self.handler.get_argument("key"))
        # Get metrics
        from_ts = datetime.datetime.now() - datetime.timedelta(seconds=1800)
        from_ts = from_ts.replace(microsecond=0)
        interface_sql = """
          SELECT
            managed_object,
            path[4] AS iface,
            argMax(speed, ts) AS speed,
            argMax(load_in, ts) AS load_in,
            argMax(load_out, ts) AS load_out,
            argMax(packets_in, ts) AS packets_in,
            argMax(packets_out, ts) AS packets_out
          FROM interface
          WHERE
            date >= toDate('%s')
            AND ts >= toDateTime('%s')
            AND (%s)
          GROUP BY managed_object, iface
        """ % (
            from_ts.date().isoformat(),
            from_ts.isoformat(sep=" "),
            " OR ".join(
                "(managed_object=%d AND path[4]='%s')" % (q[0], q[1].replace("'", "''"))
                for q in query
            ),
        )
        # Get data
        metrics = []  # type: List[Tuple[int, str, str, str]]
        ch = ch_connection()
        try:
            for (mo, iface, speed, load_in, load_out, packets_in, packets_out) in ch.execute(
                post=interface_sql
            ):
                if_hash = str(bi_hash(iface))
                metrics += [
                    (mo, if_hash, "speed", self.humanize_metric(speed)),
                    (mo, if_hash, "load_in", self.humanize_metric(load_in)),
                    (mo, if_hash, "load_out", self.humanize_metric(load_out)),
                    (mo, if_hash, "packets_in", self.humanize_metric(packets_in)),
                    (mo, if_hash, "packets_out", self.humanize_metric(packets_out)),
                ]
        except ClickhouseError:
            pass
        # Set defaults
        m_index = set()  # type: Set[Tuple[int, str]]
        for mo_bi_id, iface, _, _ in metrics:
            m_index.add((int(mo_bi_id), iface))

        interface_metrics = {"speed", "load_in", "load_out", "packets_in", "packets_out"}
        for mo_bi_id, iface in query:
            if (mo_bi_id, iface) not in m_index:
                for metric in interface_metrics:
                    metrics += [(str(mo_bi_id), str(bi_hash(iface)), metric, "+")]
        return metrics
