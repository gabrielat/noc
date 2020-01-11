# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# sa.monitor application
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python module
import re

# NOC modules
from noc.services.web.apps.sa.objectlist.views import ObjectListApplication

# from noc.core.dateutils import humanize_distance
from noc.core.scheduler.scheduler import Scheduler
from noc.sa.models.managedobject import ManagedObject
from noc.core.scheduler.job import Job
from noc.sa.models.profile import Profile
from noc.core.translation import ugettext as _


class MonitorApplication(ObjectListApplication):
    """
    sa.monitor application
    """

    title = _("Monitor")
    menu = _("Monitor")
    icon = "icon_monitor"

    rx_time = re.compile(r"Completed. Status: SUCCESS\s\((?P<time>\S+)\)", re.MULTILINE)
    job_map = {
        "noc.services.discovery.jobs.periodic.job.PeriodicDiscoveryJob": "p",
        "noc.services.discovery.jobs.box.job.BoxDiscoveryJob": "b",
    }

    def extra_query(self, q, order):
        return {}, []

    def queryset(self, request, query=None):
        r = JobF(pool="MO")
        r.mos_filter = super(MonitorApplication, self).queryset(request, query)
        return r

    def extra_data(self, data, ordering=None, start=None, limit=None):
        scheduler = Scheduler("discovery", pool="MO").get_collection()
        pipeline = [{"$match": {Job.ATTR_KEY: {"$in": list(data.values_list("id", flat=True))}}}]
        # if ordering:
        #     pipeline += [{"$sort": {self.sort_map[f]: 1 for f in ordering if f in self.sort_map}}]
        pipeline += [
            {
                "$group": {
                    "_id": "$key",
                    "jobs": {
                        "$push": {
                            "jcls": "$jcls",
                            "s": "$s",
                            "ts": "$ts",
                            "last": "$last",
                            "ldur": "$ldur",
                            "ls": "$ls",
                        }
                    },
                }
            }
        ]
        if start:
            pipeline += [{"$skip": start}]
        if limit:
            pipeline += [{"$limit": limit}]
        return scheduler.aggregate(pipeline)

    def bulk_field_managed_object(self, data):
        """
        Apply managed objects field
        :param data:
        :return:
        """
        mo_ids = [x["id"] for x in data]
        if not mo_ids:
            return data
        mos = {
            x[0]: {"name": x[1], "address": x[2], "profile_name": str(Profile.get_by_id(x[3]))}
            for x in ManagedObject.objects.filter(id__in=mo_ids).values_list(
                "id", "name", "address", "profile"
            )
        }
        for x in data:
            x.update(mos[x["id"]])
        return data

    def instance_to_dict(self, data, fields=None):
        result = {
            "id": data["_id"],
            "name": "",
            "address": "",
            "profile_name": "",
        }
        for job in data["jobs"]:
            prefix = self.job_map[job["jcls"]]
            result.update(
                {
                    "%s_time_start" % prefix: self.to_json(job[Job.ATTR_TS]),
                    "%s_last_success" % prefix: self.to_json(job.get(Job.ATTR_LAST)),
                    "%s_status" % prefix: job[Job.ATTR_STATUS] if Job.ATTR_STATUS in job else "--",
                    "%s_time" % prefix: job[Job.ATTR_LAST_DURATION],
                    "%s_duration" % prefix: job[Job.ATTR_LAST_DURATION],
                    "%s_last_status" % prefix: job.get(Job.ATTR_LAST_STATUS),
                }
            )
        return result


class JobF(object):
    def __init__(self, scheduler="discovery", pool="default"):
        self.scheduler = Scheduler(scheduler, pool=pool).get_collection()
        self.mos_filter = None
        self.pipeline = [
            {
                "$group": {
                    "_id": "$key",
                    "jobs": {
                        "$push": {
                            "jcls": "$jcls",
                            "s": "$s",
                            "ts": "$ts",
                            "last": "$last",
                            "ldur": "$ldur",
                            "ls": "$ls",
                        }
                    },
                }
            }
        ]
        pass

    def filter(self, *args, **kwargs):
        self.mos_filter = self.mos_filter.filter(**kwargs)
        return self

    def __getitem__(self, k):
        if isinstance(k, slice):
            self.pipeline += [{"$skip": k.start}]
            self.pipeline += [{"$limit": k.stop - k.start}]
        return self

    def __iter__(self):
        mos_ids = list(self.mos_filter.values_list("id", flat=True))
        self.pipeline = [{"$match": {Job.ATTR_KEY: {"$in": mos_ids}}}] + self.pipeline
        for r in self.scheduler.aggregate(self.pipeline):
            yield r
