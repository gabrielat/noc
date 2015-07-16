# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## System daemons base class
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
from __future__ import with_statement
import ConfigParser
import sys
import logging
import os
import signal
import optparse
import logging.handlers
import time
## NOC modules
from noc.lib.debug import error_report, frame_report
from noc.lib.validators import is_ipv4, is_int
from noc.lib.version import get_version
from noc.lib.log import ColorFormatter
from noc.lib.perf import enable_stats, MetricsHub

# Load netifaces to resolve interface addresses when possible
try:
    import netifaces

    USE_NETIFACES = True
except ImportError:
    USE_NETIFACES = False

_daemon = None


class Daemon(object):
    """
    Daemon base class
    """
    daemon_name = "daemon"
    defaults_config_path = "etc/%(daemon_name)s.defaults"
    config_path = "etc/%(daemon_name)s.conf"
    # Initialize custom fields and solutions
    use_solutions = False

    LOG_FORMAT = "%(asctime)s [%(name)s] %(message)s"

    LOG_LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    ## Auto-create additional metrics
    METRICS = []

    def __init__(self):
        global _daemon
        self.start_time = time.time()
        _daemon = self
        self.logger = logging.getLogger(self.daemon_name)
        # Chdir to the root of project
        os.chdir(os.path.join(os.path.dirname(sys.argv[0]), ".."))
        self.prefix = os.getcwd()
        # Parse commandline
        self.opt_parser = optparse.OptionParser()
        self.opt_parser.add_option("-c", "--config", action="store",
                                   type="string", dest="config",
                                   help="Read config from CONFIG")
        self.opt_parser.add_option("-i", "--instance", action="store",
                                   type="string", dest="instance_id",
                                   default="0",
                                   help="Set instnace id")
        self.opt_parser.add_option("-V", "--version", action="store_true",
                                   dest="show_version", default=False,
                                   help="Show daemon version")
        self.setup_opt_parser()
        self.options, self.args = self.opt_parser.parse_args()
        if self.options.show_version:
            print get_version()
            sys.exit(0)
        # Read config
        self.config = None
        self.instance_id = self.options.instance_id
        self.metrics = MetricsHub(
            "noc.%s.%s" % (self.daemon_name, self.instance_id), *self.METRICS)
        self.manhole_status = False
        self.start_delay = 0
        self.load_config()
        # Register signal handlers if any
        for s in [s for s in dir(self) if s.startswith("SIG")]:
            try:
                sig = getattr(signal, s)
            except AttributeError:
                self.logger.error(
                    "Signal '%s' is not supported on this platform" % s)
                continue
            signal.signal(sig, getattr(self, s))
        #atexit.register(self.at_exit)
        if self.use_solutions:
            self.logger.info("Initializing solutions")
            from noc.lib.solutions import init_solutions
            init_solutions()

    def parse_logsize(self, s):
        if s and s.isdigit():
            return int(s)
        if len(s) > 1:
            s = s.upper()
            i = s[:1]
            if i.isdigit():
                if s.endswith('K'):
                    return (int(i) * 1024)
                if s.endswith('M'):
                    return (int(i) * 1024 * 1024)
                if s.endswith('G'):
                    return (int(i) * 1024 * 1024 * 1024)
        return 0

    def load_config(self):
        """
        Load and process configuration files
        :return:
        """
        first_run = True
        if self.config:
            self.logger.info("Loading config")
            first_run = False
        self.config = ConfigParser.SafeConfigParser()
        if self.defaults_config_path:
            self.config.read(
                self.defaults_config_path % {"daemon_name": self.daemon_name})
        if self.options.config:
            self.config.read(self.options.config)
        elif self.config_path:
            self.config.read(
                self.config_path % {"daemon_name": self.daemon_name})
        if not first_run:
            self.on_load_config()
            # Set up logging
        if self.config.get("main", "loglevel") not in self.LOG_LEVELS:
            raise Exception(
                "Invalid loglevel '%s'" % self.config.get("main", "loglevel"))
        for h in logging.root.handlers:
            logging.root.removeHandler(h)  # Dirty hack for baseConfig
        # Log to stdout
        loglevel = self.LOG_LEVELS[self.config.get("main", "loglevel")]
        handler = logging.StreamHandler(sys.stdout)
        if self.is_stderr_supports_color():
            formatter = ColorFormatter(
                "%(color)s" + self.LOG_FORMAT + "%(endcolor)s",
                None
            )
        else:
            formatter = logging.Formatter(self.LOG_FORMAT, None)
        handler.setFormatter(formatter)
        logging.root.addHandler(handler)
        logging.root.setLevel(loglevel)
        self.setup_manhole()
        self.setup_perf()
        if self.config.has_option("main", "start_delay"):
            self.start_delay = self.config.getint("main", "start_delay")

    def setup_manhole(self):
        to_start_manhole = (
            self.config.has_section("debug") and
            self.config.has_option("debug", "enable_manhole") and
            self.config.getboolean("debug", "enable_manhole")
        )
        if to_start_manhole and not self.manhole_status:
            import manhole
            manhole.logger = logging.getLogger(self.daemon_name + ".manhole")
            self.logger.info("Opening manhole")
            manhole.install()
            self.manhole_status = True

    def setup_perf(self):
        kwargs = {"enabled": False}
        if self.config.has_section("debug"):
            if (self.config.has_option("debug", "enable_timing") and
                    self.config.getboolean("debug", "enable_timing")):
                kwargs["enabled"] = True
                kwargs["base_dir"] = self.config.get("debug", "timing_base")
            if (self.config.has_option("debug", "enable_reports") and
                    self.config.getboolean("debug", "enable_reports")):
                kwargs["report_collector"] = self.config.get(
                    "debug", "report_collector")
                kwargs["report_interval"] = self.config.getint(
                    "debug", "report_interval")
        enable_stats(**kwargs)

    def die(self, msg):
        self.logger.error(msg)
        self.at_exit()
        os._exit(1)

    def check_writable(self, path):
        """
        Check file can be open as writable
        :return:
        """
        try:
            f = open(path, "a")
        except IOError, why:
            sys.stderr.write(str(why) + "\n")
            sys.stderr.write("Exiting\n")
            os._exit(1)

    def on_load_config(self):
        """
        Called after config has been reloaded on SIGHUP
        :return:
        """
        pass

    def run(self):
        """
        Main daemon loop. Must be overriden
        :return:
        """
        pass

    def resolve_address(self, s):
        """
        Resolve interface names to IP addresses
        :param s: Interface name or IPv4 address
        :return:
        """
        if is_ipv4(s):
            return s
        if USE_NETIFACES:
            try:
                a = netifaces.ifaddresses(s)
            except ValueError:
                raise Exception("Invalid interface '%s'" % s)
            try:
                return a[2][0]["addr"]
            except (IndexError, KeyError):
                raise Exception("No ip address for interface: '%s' found" % s)
        raise Exception("Cannot resolve address '%s'" % s)

    def resolve_addresses(self, addr_list, default_port):
        """
        Parses string and returns a list of (ip,port)
        :param addr_list: Comma-separared list of addresses in form:
                          * ip
                          * ip:port
                          * interface
                          * interface:port
        :param default_port:
        :return:
        """
        r = []
        for x in addr_list.split(","):
            x = x.strip()
            if not x:
                continue
            if ":" in x:  # Implicit port notation
                x, port = x.split(":", 1)
                if is_int(port):
                    port = int(port)
                else:
                    import socket
                    try:
                        port = socket.getservbyname(port)
                    except socket.error:
                        raise Exception("Invalid port: %s" % port)
            else:
                port = int(default_port)
            if port <= 0 or port > 65535:
                raise Exception("Invalid port: %s" % port)
            if is_ipv4(x):
                r += [(x, port)]
                continue
            if USE_NETIFACES:  # Can resolve interface names
                try:
                    a = netifaces.ifaddresses(x)
                except ValueError:
                    raise Exception("Invalid interface '%s'" % x)
                try:
                    x = a[2][0]["addr"]
                except (IndexError, KeyError):
                    self.logger.error(
                        "No ip address for interface: '%s' found", x
                    )
                    continue
                r += [(x, port)]
                continue
            raise Exception("Cannot resolve address '%s'" % x)
        return r

    def setup_opt_parser(self):
        """
        Add additional options to setup_opt_parser
        :return:
        """
        pass

    def process_command(self):
        """
        Process self.args[0] command
        :return:
        """
        self.guarded_run()

    def guarded_run(self):
        """
        Run daemon and catch common exceptions
        :return:
        """
        if self.start_delay:
            self.logger.info("Delaying start for %s seconds",
                             self.start_delay)
            time.sleep(self.start_delay)
        try:
            self.run()
        except KeyboardInterrupt:
            pass
        except MemoryError:
            self.logger.error("Out of memory. Exiting.")
        except SystemExit:
            self.logger.info("Exiting")
        except:
            error_report()
        self.at_exit()

    def at_exit(self):
        self.logger.info("STOP")

    def is_stderr_supports_color(self):
        """
        Check stderr is TTY and supports color
        """
        try:
            import curses
        except ImportError:
            return False
        if hasattr(sys.stderr, "isatty") and sys.stderr.isatty():
            try:
                curses.setupterm()
                if curses.tigetnum("colors") > 0:
                    return True
            except Exception:
                pass
        return False

    def SIGUSR2(self, signo, frame):
        """
        Dump current execution frame trace on SIGUSR2
        :param signo:
        :param frame:
        :return:
        """
        frames = sys._current_frames().items()
        if len(frames) == 1:
            # Single thread
            frame_report(frame)
        else:
            # Multi-threaded
            import threading

            for tid, frame in frames:
                if tid in threading._active:
                    caption = "Thread: name=%s id=%s" % (
                    threading._active[tid].getName(), tid)
                else:
                    caption = "Unknown thread: id=%s" % tid
                frame_report(frame, caption)

    def SIGHUP(self, signo, frame):
        """
        Reload config on SIGHUP
        :param signo:
        :param frame:
        :return:
        """
        self.load_config()

    def SIGINT(self, signo, frame):
        """
        ^C processing
        :param signo:
        :param frame:
        :return:
        """
        self.logger.info("SIGINT received. Exiting")
        self.at_exit()
        os._exit(0)

    def SIGTERM(self, signo, frame):
        """
        SIGTERM processing
        :param signo:
        :param frame:
        :return:
        """
        self.logger.info("SIGTERM received. Exiting")
        self.at_exit()
        os._exit(0)
