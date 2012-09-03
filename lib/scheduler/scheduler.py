# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Scheduler Job Class
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import logging
import time
import datetime
## NOC modules
from error import JobExists
from noc.lib.nosql import get_db
from noc.lib.debug import error_report, get_traceback
from noc.sa.models import ReduceTask


class Scheduler(object):
    COLLECTION_BASE = "noc.schedules."
    ATTR_TS = "ts"
    ATTR_CLASS = "jcls"
    ATTR_STATUS = "s"
    ATTR_TIMEOUT = "timeout"
    ATTR_KEY = "key"
    ATTR_DATA = "data"
    ATTR_SCHEDULE = "schedule"
    ATTR_LAST = "last"  # last run
    ATTR_LAST_STATUS = "ls"  # last completion status
    ATTR_LAST_DURATION = "ldur"  # last job duration
    ATTR_RUNS = "runs"  # Number of runs
    ATTR_TRACEBACK = "tb"  # Last error traceback
    ATTR_LOG = "log"  # Job log
    S_WAIT = "W"  # Waiting to run
    S_RUN = "R"   # Running
    S_STOP = "S"  # Stopped by operator
    S_FAIL = "F"  # Not used yet

    JobExists = JobExists

    def __init__(self, name, cleanup=None, reset_running=False):
        self.name = name
        self.job_classes = {}
        self.collection_name = self.COLLECTION_BASE + self.name
        self.collection = get_db()[self.collection_name]
        self.active_mrt = {}  # ReduceTask -> Job instance
        self.cleanup_callback = cleanup
        self.reset_running = reset_running

    def debug(self, msg):
        logging.debug("[%s] %s" % (self.name, msg))

    def info(self, msg):
        logging.info("[%s] %s" % (self.name, msg))

    def error(self, msg):
        logging.error("[%s] %s" % (self.name, msg))

    def register_job_class(self, cls):
        self.info("Registering job class: %s" % cls.name)
        self.job_classes[cls.name] = cls

    def get_job_class(self, name):
        return self.job_classes[name]

    def submit(self, job_name, key=None, data=None,
               schedule=None, ts=None):
        """
        Submit new job
        """
        if ts is None:
            ts = datetime.datetime.now()
        elif type(ts) in (int, long, float):
            ts = (datetime.datetime.now() +
                  datetime.timedelta(seconds=ts))
        # Check Job is not exists
        if self.collection.find_one({
            self.ATTR_CLASS: job_name,
            self.ATTR_KEY: key
        }):
            raise JobExists()
        # Submit job
        id = self.collection.insert({
            self.ATTR_TS: ts,
            self.ATTR_CLASS: job_name,
            self.ATTR_STATUS: self.S_WAIT,
            self.ATTR_KEY: key,
            self.ATTR_DATA: data,
            self.ATTR_SCHEDULE: schedule
        }, manipulate=True, safe=True)
        self.info("Scheduling job %s(%s) id=%s at %s" % (
            job_name, key, id, ts))

    def remove_job(self, job_name, key):
        self.info("Removing job %s(%s)" % (job_name, key))
        self.collection.remove({
            self.ATTR_CLASS: job_name,
            self.ATTR_KEY: key
        }, safe=True)

    def reschedule_job(self, job_name, key, ts, status=None,
                       duration=None, last_status=None, tb=None,
                       log=None, update_runs=False):
        self.info("Rescheduling job %s(%s) to %s%s" % (
            job_name, key, ts, " status=%s" % status if status else ""))
        s = {
            self.ATTR_TS: ts,
            self.ATTR_TRACEBACK: tb,
            self.ATTR_LOG: log or []
        }
        if status:
            s[self.ATTR_STATUS] = status
        if last_status:
            s[self.ATTR_LAST_STATUS] = last_status
        if duration is not None:
            s[self.ATTR_LAST_DURATION] = duration
        op = {"$set": s}
        if update_runs:
            op["$inc"] = {self.ATTR_RUNS: 1}
        self.collection.update({
            self.ATTR_CLASS: job_name,
            self.ATTR_KEY: key
        }, op, safe=True)

    def set_job_status(self, job_name, key, status):
        self.info("Changing %s(%s) status to %s" % (
            job_name, key, status))
        self.collection.update({
            self.ATTR_CLASS: job_name,
            self.ATTR_KEY: key
        }, {
            "$set": {self.ATTR_STATUS: status}
        }, safe=True)

    def run_job(self, job):
        """
        Begin job execution
        :param job:
        :return:
        """
        # Dereference job
        if not job.dereference():
            logging.info("Cannot dereference job %s(%s). Removing" % (
                job.name, job.key))
            self.remove_job(job.name, job.key)
            return
        # Change status
        self.info("Running job %s(%s)" % (job.name, job.key))
        job.started = time.time()
        self.collection.update({
            self.ATTR_CLASS: job.name,
            self.ATTR_KEY: job.key
        }, {"$set": {
            self.ATTR_STATUS: self.S_RUN,
            self.ATTR_LAST: datetime.datetime.fromtimestamp(job.started)
        }})
        #
        if job.map_task:
            # Run in MRT mode
            t = ReduceTask.create_task(
                job.get_managed_object(),  # Managed object is in key
                None, {},
                job.map_task, job.get_map_task_params()
            )
            self.active_mrt[t] = job
        else:
            self._run_job_handler(job)

    def _run_job_handler(self, job, **kwargs):
        tb = None
        try:
            r = job.handler(**kwargs)
        except Exception:
            error_report()
            job.on_exception()
            s = job.S_EXCEPTION
            tb = get_traceback()
        else:
            if r:
                self.info("Job %s(%s) is completed successfully" % (
                    job.name, job.key))
                job.on_success()
                s = job.S_SUCCESS
            else:
                self.info("Job %s(%s) is failed" % (
                    job.name, job.key))
                job.on_failure()
                s = job.S_FAILED
        #
        t = job.get_schedule(s)
        if t is None:
            # Unschedule job
            self.remove_job(job.name, job.key)
        else:
            # Reschedule job
            t1 = time.time()
            self.reschedule_job(
                job.name, job.key, t,
                status="W",
                last_status=s,
                duration=t1 - job.started,
                tb=tb,
                update_runs=True
            )

    def complete_mrt_job(self, t):
        job = self.active_mrt[t]
        for m in t.maptask_set.all():
            if m.status == "C":
                self._run_job_handler(job, object=m.managed_object,
                    result=m.script_result)
        t.delete()

    def run_pending(self):
        n = 0
        # Check for complete MRT
        if self.active_mrt:
            complete = [t for t in self.active_mrt if t.complete]
            for t in complete:
                self.complete_mrt_job(t)
            self.active_mrt = dict(
                (t, self.active_mrt[t])
                    for t in self.active_mrt if t not in complete)
        # Check for pending persistent tasks
        for job_data in self.collection.find({
            self.ATTR_TS: {"$lte": datetime.datetime.now()},
            self.ATTR_STATUS: self.S_WAIT
            }):
            jcls = self.job_classes.get(job_data[self.ATTR_CLASS])
            if not jcls:
                # Invalid job class. Park job to FAIL state
                self.error("Invalid job class: %s" % jcls)
                self.set_job_status(job_data[self.ATTR_CLASS],
                    job_data[self.ATTR_KEY], self.S_FAIL)
                continue
            job = jcls(self,
                job_data[self.ATTR_KEY], job_data[self.ATTR_DATA],
                job_data[self.ATTR_SCHEDULE]
            )
            self.run_job(job)
            n += 1
        return n

    def run(self):
        if self.reset_running:
            # Change running to waiting
            self.debug("Resetting running jobs")
            self.collection.update({
                self.ATTR_STATUS: self.S_RUN
            }, {
                "$set": {self.ATTR_STATUS: self.S_WAIT}
            }, multi=True, safe=True)
        self.info("Running scheduler")
        while True:
            if not self.run_pending():
                time.sleep(1)
            else:
                self.cleanup()

    def wipe(self):
        """
        Wipe off all schedules
        """
        self.collection.drop()

    def cleanup(self):
        if self.cleanup_callback:
            self.cleanup_callback()
