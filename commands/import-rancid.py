# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Import managed objects from rancid
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import logging
import subprocess
import re
import datetime
import os

# Third-party modules
from django.db.models import Q

# Third-party modules
import pytz

# NOC modules
from noc.core.management.base import BaseCommand, CommandError
from noc.core.mongo.connection import connect
from noc.sa.models.administrativedomain import AdministrativeDomain
from noc.main.models.pool import Pool
from noc.sa.models.managedobjectprofile import ManagedObjectProfile
from noc.sa.models.profile import Profile
from noc.sa.models.managedobject import ManagedObject
from noc.core.gridvcs.manager import GridVCS
from noc.core.script.scheme import TELNET, SSH
import noc.settings


class Command(BaseCommand):
    """
    Manage Jobs
    """

    logger = logging.getLogger("main")
    TZ = pytz.timezone(noc.settings.TIME_ZONE)
    TMP = "/tmp/noc-import-rancid"

    help = "Import data from rancid"

    def add_arguments(self, parser):

        parser.add_argument(
            parser.add_argument(
                "--routerdb", action="append", dest="routerdb", help="Path to the router.db"
            ),
            parser.add_argument(
                "--cloginrc", action="append", dest="cloginrc", help="Path to the .cloginrc"
            ),
            parser.add_argument(
                "--hosts", action="append", dest="hosts", help="Path to the /etc/hosts"
            ),
            parser.add_argument("--repo", action="store", dest="repo", help="CVS repository"),
            parser.add_argument(
                "--repo-prefix",
                action="store",
                dest="repoprefix",
                help="File path prefix to checkout from repo",
            ),
            parser.add_argument(
                "--dry-run",
                action="store_true",
                dest="dry_run",
                help="Check only, do not write to database",
            ),
            parser.add_argument(
                "--tags", action="append", dest="tags", help="Mark created managed objects by tags"
            ),
            parser.add_argument(
                "--profile",
                action="store",
                dest="object_profile",
                help="Set managed object profile for created objects",
                default="default",
            ),
            parser.add_argument(
                "--domain",
                action="store",
                dest="domain",
                help="Set administrative domain for created objects",
                default="default",
            ),
            parser.add_argument(
                "--pool",
                action="store",
                dest="pool",
                help="Set pool for created objects",
                default="default",
            ),
            parser.add_argument(
                "--shard", action="store", dest="shard", help="Shard import to separate processes"
            ),
        )

    PROFILE_MAP = {
        "cisco": Profile.get_by_name("Cisco.IOS"),
        "juniper": Profile.get_by_name("Juniper.JUNOS"),
    }

    rx_f = re.compile(r"^RCS file: (?P<file>.+?),v$", re.MULTILINE | re.DOTALL)

    rx_fn = re.compile(r"^Working file: (?P<fn>.+?)$", re.MULTILINE | re.DOTALL)

    rx_rev = re.compile(
        r"^-----+\n"
        r"revision (?P<rev>\S+)\n"
        r"date: (?P<date>\S+ \S+(?: \S+)?);.+? state: (?P<state>\S+)",
        re.MULTILINE | re.DOTALL,
    )

    # Regular expresion to split config
    # Config is a final part
    SPLIT_MAP = {
        "Cisco.IOS": re.compile(r"^\n", re.MULTILINE),
        "Juniper.JUNOS": re.compile(r"^#[^#>\n]+> show configuration\s*\n", re.MULTILINE),
    }

    def parse_hosts(self, hosts):
        """
        Parse /etc/hosts
        :returns: dict of name -> ip
        """
        r = {}
        for path in hosts:
            self.logger.info("Reading hosts from %s", path)
            with open(path) as f:
                for line in f.readlines():
                    if "#" in line:
                        line = line.split("#", 1)[0]
                    line = line.strip()
                    if not line:
                        continue
                    if ":" in line:
                        # Skip IPv6
                        continue
                    parts = line.split()
                    for p in parts[1:]:
                        r[p] = parts[0]
        return r

    def parse_routerdb(self, routerdb):
        rdb = {}  # Name -> profile
        for path in routerdb:
            self.logger.info("Reading routers from %s", path)
            with open(path) as f:
                for line in f.readlines():
                    if "#" in line:
                        line = line.split("#", 1)[0]
                    line = line.strip()
                    if not line:
                        continue
                    r = line.split(":")
                    if len(r) != 3:
                        continue
                    name, t, s = r
                    if s != "up":
                        self.logger.debug("Skipping %s", name)
                        continue
                    p = self.PROFILE_MAP.get(t)
                    if not p:
                        self.logger.info("Unknown type '%s'. Skipping", t)
                        continue
                    rdb[name] = p
        return rdb

    def parse_cloginrc(self, cloginrc):
        login = {}
        defaults = {}
        for path in cloginrc:
            self.logger.info("Reading cloginrc from %s", path)
            with open(path) as f:
                for line in f.readlines():
                    if "#" in line:
                        line = line.split("#", 1)[0]
                    line = line.strip()
                    if not line:
                        continue
                    line = line.replace("\t", " ")
                    r = line.split()
                    if len(r) > 4:
                        op, v, host = r[:3]
                        value = " ".join(r[3:])
                    elif len(r) == 3:
                        op, v, value = r
                        defaults[v] = value
                        continue
                    else:
                        op, v, host, value = r
                    if op != "add":
                        continue
                    if host not in login:
                        login[host] = {}
                    login[host][v] = value
        return login, defaults

    def index_cvs(self, repo):
        r = {}  # path -> (revision, date)
        p = subprocess.Popen(["cvs", "log"], cwd=repo, stdout=subprocess.PIPE)
        data = p.stdout.read()
        parts = self.rx_f.split(data)[2::2]
        for data in parts:
            match = self.rx_fn.search(data)
            if not match:
                continue
            fn = match.group("fn")
            r[fn] = []
            for match in self.rx_rev.finditer(data):
                # if match.group("state").lower() == "dead":
                #    continue  # Ignore object replacement
                rev = match.group("rev")
                date = match.group("date")
                ds = date.split()
                if "/" in ds[0]:
                    fmt = "%Y/%m/%d %H:%M:%S"
                else:
                    fmt = "%Y-%m-%d %H:%M:%S"
                if len(ds) == 3:
                    # Date with TZ
                    date = "%s %s" % (ds[0], ds[1])
                r[fn] += [
                    (
                        rev,
                        self.TZ.normalize(pytz.utc.localize(datetime.datetime.strptime(date, fmt))),
                    )
                ]
        return r

    def handle(self, *args, **options):
        connect()
        if options["verbosity"] >= 2:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        for h in self.logger.handlers:
            h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        if not options["routerdb"]:
            raise CommandError("No routerdb given")
        if not options["cloginrc"]:
            raise CommandError("No cloginrc given")
        if not options["hosts"]:
            options["hosts"] = ["/etc/hosts"]
        if not options["repo"]:
            raise CommandError("No CVS repository")
        repo_prefix = options.get("repoprefix") or ""
        if not options["object_profile"]:
            raise CommandError("No object profile set")
        try:
            object_profile = ManagedObjectProfile.objects.get(
                name=options["object_profile"].strip()
            )
        except ManagedObjectProfile.DoesNotExist:
            raise CommandError("Invalid object profile: %s" % options["object_profile"])
        if not options["domain"]:
            raise CommandError("No administrative domain set")
        try:
            domain = AdministrativeDomain.objects.get(name=options["domain"].strip())
        except AdministrativeDomain.DoesNotExist:
            raise CommandError("Invalid administrative domain: %s" % options["domain"])
        if not options["pool"]:
            raise CommandError("No pool set")
        try:
            pool = Pool.objects.get(name=options["domain"].strip())
        except Pool.DoesNotExist:
            raise CommandError("Invalid pool: %s" % options["pool"])
        shard_member = 0
        shard_members = 0
        if options.get("shard"):
            shard = options["shard"]
            if "/" not in shard:
                raise CommandError("Shard must be <member>/<members>")
            shard_member, shard_members = [int(x) for x in shard.split("/")]
        tags = []
        if options["tags"]:
            for t in options["tags"]:
                tags += [x.strip() for x in t.split(",")]
        self.dry_run = bool(options["dry_run"])
        #
        if not os.path.isdir(self.TMP):
            os.mkdir(self.TMP)
        #
        revisions = self.index_cvs(options["repo"])
        # Read configs
        hosts = self.parse_hosts(options["hosts"])
        rdb = self.parse_routerdb(options["routerdb"])
        login, ldefaults = self.parse_cloginrc(options["cloginrc"])
        # Process data
        n = 0
        count = len(rdb)
        for name in sorted(rdb):
            if shard_members:
                if n % shard_members != shard_member:
                    n += 1
                    continue  # Processed by other shard
            self.logger.debug("[%s/%s] Processing host %s", n, count, name)
            n += 1
            profile = Profile.get_by_name(rdb[name])
            address = hosts.get(name)
            if not address:
                # @todo: Resolve
                self.logger.info("Cannot resolve address for %s. Skipping", name)
                continue
            ld = login.get(name, ldefaults)
            if not ld:
                self.logger.info("No credentials for %s. Skipping", name)
                continue
            user = ld.get("user")
            password = ld.get("password")
            if "method" in ld and "ssh" in ld["method"]:
                method = "ssh"
            else:
                method = "telnet"
            self.logger.info(
                "Managed object found: %s (%s, %s://%s@%s/)",
                name,
                profile.name,
                method,
                user,
                address,
            )
            if not self.dry_run:
                try:
                    mo = ManagedObject.objects.get(Q(name=name) | Q(address=address))
                    self.logger.info("Already in the database")
                except ManagedObject.DoesNotExist:
                    self.logger.info("Creating managed object %s", name)
                    mo = ManagedObject(
                        name=name,
                        object_profile=object_profile,
                        administrative_domain=domain,
                        pool=pool,
                        scheme=SSH if method == "ssh" else TELNET,
                        address=address,
                        profile=profile,
                        user=user,
                        password=password,
                        trap_source_ip=address,
                        tags=tags,
                    )
                    mo.save()
            if name not in revisions:
                self.logger.error("Cannot find config for %s", name)
                continue
            if not self.dry_run:
                self.import_revisions(options["repo"], repo_prefix, mo, name, revisions[name])

    def get_diff(self, repo, name, r0, r1):
        p = subprocess.Popen(
            ["cvs", "diff", "-r%s" % r0, "-r%s" % r1, name], cwd=repo, stdout=subprocess.PIPE
        )
        return p.stdout.read()

    def import_revisions(self, repo, repo_prefix, mo, name, revisions):
        """
        Import CVS file revisions
        """

        def write_file(path, data):
            with open(path, "w") as f:
                f.write(data)

        path = os.path.join(self.TMP, name)
        lr = len(revisions)
        n = 1
        gridvcs = GridVCS("config")
        split_re = self.SPLIT_MAP[mo.profile.name]
        for rev, ts in reversed(revisions):
            self.logger.debug("%s: importing rev %s [%s/%s]", name, rev, n, lr)
            n += 1
            try:
                subprocess.check_call(
                    "cvs co -p -r%s -f %s > %s" % (rev, os.path.join(repo_prefix, name), path),
                    cwd=repo,
                    shell=True,
                )
            except subprocess.CalledProcessError as e:
                self.logger.error("Failed to import %s@%s. Skipping", name, rev)
                self.logger.error("CVS reported: %s", e)
                continue
            if not self.dry_run:
                with open(path, "r") as f:
                    data = f.read()
                # Strip config
                data = split_re.split(data, 1)[-1]
                # Save to GridVCS
                gridvcs.put(mo.id, data, ts=ts)
        if os.path.exists(path):
            os.unlink(path)


if __name__ == "__main__":
    Command().run()
