# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# escalation command
# ----------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import print_function
import argparse
import operator
# NOC modules
from noc.core.management.base import BaseCommand
from noc.fm.models.alarmescalation import AlarmEscalation
from noc.sa.models.selectorcache import SelectorCache
from noc.fm.models.utils import get_alarm
from noc.sa.models.managedobjectprofile import ManagedObjectProfile
from noc.sa.models.serviceprofile import ServiceProfile
from noc.crm.models.subscriberprofile import SubscriberProfile
from noc.fm.models.activealarm import ActiveAlarm
from noc.fm.models.archivedalarm import ArchivedAlarm


class Command(BaseCommand):
    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="cmd")
        #
        check_parser = subparsers.add_parser("check")
        check_parser.add_argument(
            "check_alarms",
            nargs=argparse.REMAINDER,
            help="Checks alarms escalation"
        )
        #
        apply_parser = subparsers.add_parser("run")
        apply_parser.add_argument(
            "run_alarms",
            nargs=argparse.REMAINDER,
            help="Run alarm escalations"
        )

    def handle(self, cmd, *args, **options):
        return getattr(self, "handle_%s" % cmd)(*args, **options)

    def handle_check(self, check_alarms=None, *args, **kwargs):
        check_alarms = check_alarms or []
        for a_id in check_alarms:
            alarm = get_alarm(a_id)
            if alarm:
                self.check_alarm(alarm)
            else:
                self.print(
                    "ERROR: Alarm %s is not found. Skipping" % alarm
                )

    def handle_run(self, run_alarms=None, *args, **kwargs):
        run_alarms = run_alarms or []
        for a_id in run_alarms:
            alarm = get_alarm(a_id)
            if alarm and alarm.status == "A":
                self.run_alarm(alarm)
            elif alarm:
                self.print(
                    "ERROR: Alarm %s is cleared. Skipping" % alarm
                )
            else:
                self.print(
                    "ERROR: Alarm %s is not found. Skipping" % alarm
                )

    def check_alarm(self, alarm):
        def summary_to_list(summary, model):
            r = []
            for k in summary:
                p = model.get_by_id(k.profile)
                if not p or getattr(p, "show_in_summary", True) == False:
                    continue
                r += [{
                    "profile": p.name,
                    "summary": k.summary
                }]
            return sorted(r, key=lambda x: -x["summary"])

        def iter_consequences(alarm):
            """
            Generator yielding all consequences alarm
            """
            for ac in [ArchivedAlarm, ActiveAlarm]:
                for a in ac.objects.filter(root=alarm.id):
                    yield a
                    for ca in a.iter_consequences():
                        yield ca

        def iter_affected(alarm):
            """
            Generator yielding all affected managed objects
            """
            seen = set([alarm.managed_object])
            yield alarm.managed_object
            for a in iter_consequences(alarm):
                if a.managed_object not in seen:
                    seen.add(a.managed_object)
                    yield a.managed_object

        def iter_escalated(alarm):
            """
            Generator yielding all escalated consequences
            """
            for a in iter_consequences(alarm):
                if a.escalation_tt:
                    yield a

        mo = alarm.managed_object
        self.print("-" * 72)
        self.print("Alarm Id : %s  Time: %s" % (
            alarm.id, alarm.timestamp
        ))
        self.print("Class    : %s" % alarm.alarm_class.name)
        self.print("Object   : %s  Platform: %s  IP: %s" % (
            mo.name, mo.platform, mo.address
        ))
        c = mo.administrative_domain
        adm_domains = [c]
        while c.parent:
            c = c.parent
            adm_domains.insert(0, c)
        self.print(
            "Adm. Dom.: %s (%s)" % (
                " | ".join(c.name for c in adm_domains),
                " | ".join(str(c.id) for c in adm_domains)
            )
        )
        escalations = list(AlarmEscalation.objects.filter(
            alarm_classes__alarm_class=alarm.alarm_class.id
        ))
        if not escalations:
            self.print("@ No matched escalations")
            return
        for esc in escalations:
            self.print("[Chain: %s]" % esc.name)
            if alarm.root:
                self.print("    @ Not a root cause (Root Id: %s)" % alarm.root)
                continue
            for e in esc.escalations:
                self.print("    [After %ss]" % e.delay)
            # Check administrative domain
            if (e.administrative_domain and
                    e.administrative_domain.id not in alarm.adm_path):
                self.print("    @ Administrative domain mismatch (%s not in %s)" % (
                    e.administrative_domain.id, alarm.adm_path
                ))
                continue
            # Check severity
            if e.min_severity and alarm.severity < e.min_severity:
                self.print("    @ Severity mismatch: %s < %s" % (
                    alarm.severity, e.min_severity))
                continue
            # Check selector
            if e.selector and not SelectorCache.is_in_selector(mo, e.selector):
                self.print("    @ Selector mismatch (%s required)" % (
                    e.selector.name))
                continue
            # Check time pattern
            if e.time_pattern and not e.time_pattern.match(alarm.timestamp):
                self.print("    @ Time pattern mismatch (%s required)" % (
                    e.time_pattern.name))
                continue
            # Render escalation message
            if not e.template:
                self.print("    @ No escalation template")
                continue
            # Check whether consequences has escalations
            cons_escalated = sorted(iter_escalated(alarm),
                                    key=operator.attrgetter("timestamp"))
            affected_objects = sorted(iter_affected(alarm),
                                      key=operator.attrgetter("name"))
            #
            ctx = {
                "alarm": alarm,
                "affected_objects": affected_objects,
                "cons_escalated": cons_escalated,
                "total_objects": summary_to_list(alarm.total_objects, ManagedObjectProfile),
                "total_subscribers": summary_to_list(alarm.total_subscribers, SubscriberProfile),
                "total_services": summary_to_list(alarm.total_services, ServiceProfile),
                "tt": None
            }
            if e.create_tt:
                self.print("    Creating TT")
                if not mo.can_escalate():
                    self.print("    @ Cannot find TT System")
                    continue
                tt_system = mo.tt_system
                tts = tt_system.get_system()
                self.print("    TT System: %s  Mapped Id: %s" % (
                    tt_system.name, mo.tt_system_id
                ))
                subject = e.template.render_subject(**ctx)
                body = e.template.render_body(**ctx)
                self.print("    @ Create network TT")
                self.print("    | Subject: %s" % subject)
                self.print("    |")
                self.print("    | %s" % body.replace("\n", "\n    | "))
                tt_id = "<NETWORK TT>"
                ctx["tt"] = "%s:%s" % (tt_system.name, tt_id)
                # alarm.escalate(ctx["tt"], close_tt=e.close_tt)
                if tts.promote_group_tt:
                    self.print("    Promoting group TT")
                    self.print("    @ Create Group TT")
                    # Add objects
                    for o in alarm.iter_affected():
                        if o.can_escalate():
                            if o.tt_system == mo.tt_system:
                                self.print("    @ Add to group TT %s. Remote Id: %s" % (
                                    o.name, o.tt_system_id))
                            else:
                                self.print("    @ Cannot add to group TT. Belongs to other TT system" % o.name)
                        else:
                            self.print("    @ Cannot add to group TT %s. Escalations are disabled" % (
                                o.name
                            ))

    def run_alarm(self, alarm):
        AlarmEscalation.watch_escalations(alarm)


if __name__ == "__main__":
    Command().run()
