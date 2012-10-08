# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Scheduler utilities
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import datetime
## NOC modules
from scheduler import Scheduler
from noc.lib.nosql import get_db


def refresh_schedule(scheduler_name, job_class, key, ts=None, delta=None):
    """
    :param scheduler_name:
    :param job_class:
    :param key:
    :param ts:
    :param delta:
    :return:
    """
    if ts is None:
        ts = datetime.datetime.now()
        if delta:
            ts += datetime.timedelta(seconds=delta)
    c = get_db()["noc.schedules.%s" % scheduler_name]
    c.update({
        Scheduler.ATTR_CLASS: job_class,
        Scheduler.ATTR_KEY: key,
        Scheduler.ATTR_STATUS: Scheduler.S_WAIT
    }, {
        "$set": {Scheduler.ATTR_TS: ts}
    })


def submit_job(scheduler_name, job_class, key=None,
               ts=None, delta=None, data=None):
    if ts is None:
        ts = datetime.datetime.now()
        if delta:
            ts += datetime.timedelta(seconds=delta)
    c = get_db()["noc.schedules.%s" % scheduler_name]
    c.insert({
        Scheduler.ATTR_CLASS: job_class,
        Scheduler.ATTR_KEY: key,
        Scheduler.ATTR_STATUS: Scheduler.S_WAIT,
        Scheduler.ATTR_TS: ts,
        Scheduler.ATTR_DATA: data,
        Scheduler.ATTR_SCHEDULE: None
    })


def sliding_job(scheduler_name, job_class, key=None,
               ts=None, delta=None, data=None, cutoff_delta=0):
    #
    if ts is None:
        ts = datetime.datetime.now()
        if delta:
            ts += datetime.timedelta(seconds=delta)
    # Check the job exists
    now = datetime.datetime.now()
    c = get_db()["noc.schedules.%s" % scheduler_name]
    j = c.find_one({
        Scheduler.ATTR_CLASS: job_class,
        Scheduler.ATTR_KEY: key
    })
    if j:
        cutoff = j[Scheduler.ATTR_SCHEDULE]["cutoff"]
        if ts <= cutoff:
            # Slide job
            c.update({
                "_id": j["_id"]
            }, {
                "$set": {
                    Scheduler.ATTR_TS: ts
                }
            })
    else:
        # Submit job
        cutoff = now + datetime.timedelta(seconds=cutoff_delta)
        c.insert({
            Scheduler.ATTR_CLASS: job_class,
            Scheduler.ATTR_KEY: key,
            Scheduler.ATTR_STATUS: Scheduler.S_WAIT,
            Scheduler.ATTR_TS: ts,
            Scheduler.ATTR_DATA: data,
            Scheduler.ATTR_SCHEDULE: {
                "cutoff": cutoff
            }
        })


def sync_request(channels, request, object=None, delta=None):
    if not channels:
        return
    data = {
        "request": request,
        "channels": channels
    }
    if object:
        data["object"] = object
    submit_job("main.jobs", "main.sync_request", data=data, delta=delta)
