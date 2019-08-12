# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Vendor: EdgeCore
# OS:     ES
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
from collections import defaultdict

# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "EdgeCore.ES"
    pattern_unprivileged_prompt = r"^(?P<hostname>[^\n]+)>"
    pattern_syntax_error = r"% Invalid input detected at|% Incomplete command"
    command_super = "enable"
    pattern_prompt = r"^(?P<hostname>[^\n]+)(?:\(config[^)]*\))?#"
    pattern_more = [
        (r"---?More---?", " "),
        (r"--- \[Space\] Next page, \[Enter\] Next line, \[A\] All, Others to exit ---", " "),
        (r"Are you sure to delete non-active file", "Y\n\n"),
        (r"Startup configuration file name", "\n\n\n"),
    ]
    config_volatile = ["\x08+"]
    rogue_chars = ["\r"]
    command_submit = "\r"
    command_enter_config = "configure"
    command_leave_config = "end"
    command_save_config = "copy running-config startup-config"
    convert_mac = BaseProfile.convert_mac_to_dashed
    config_tokenizer = "indent"
    config_tokenizer_settings = {
        "line_comment": "!",
        "rewrite": [(re.compile("^queue mode"), " queue mode")],
    }
    config_normalizer = "ESNormalizer"
    confdb_defaults = [
        ("hints", "interfaces", "defaults", "admin-status", True),
        ("hints", "protocols", "lldp", "status", True),
        ("hints", "protocols", "spanning-tree", "status", False),
        ("hints", "protocols", "spanning-tree", "priority", "32768"),
        ("hints", "protocols", "loop-detect", "status", True),
        ("hints", "protocols", "ntp", "mode", "server"),
        ("hints", "protocols", "ntp", "version", "3"),
    ]
    rx_if_snmp_eth = re.compile(
        r"^Ethernet Port on Unit (?P<unit>\d+), port (?P<port>\d+)$", re.IGNORECASE
    )

    def convert_interface_name(self, s):
        """
        >>> Profile().convert_interface_name("Eth 1/ 1")
        'Eth 1/1'
        >>> Profile().convert_interface_name("Ethernet Port on unit 1, port 21")
        'Eth 1/21'
        >>> Profile().convert_interface_name("Port12")
        'Eth 1/12'
        >>> Profile().convert_interface_name("ethernet 1/1")
        'Eth 1/1'
        """
        s = s.strip()
        if s.startswith("Port"):
            return "Eth 1/%s" % s[4:].strip()
        if s.startswith("ethernet "):
            return "Eth %s" % s[9:].strip()
        match = self.rx_if_snmp_eth.match(s)
        if match:
            return "Eth %s/%s" % (match.group("unit"), match.group("port"))
        s = s.replace("  ", " ")
        return s.replace("/ ", "/")

    def setup_session(self, script):
        try:
            script.cli("terminal length 0")
        except script.CLISyntaxError:
            pass

    @staticmethod
    def parse_ifaces(e=""):
        # Parse display interfaces output command for Huawei
        r = defaultdict(dict)
        current_iface = ""
        for line in e.splitlines():
            if not line or "===" in line:
                continue
            line = line.strip()
            if (
                line.startswith("LoopBack")
                or line.startswith("MEth")
                or line.startswith("Ethernet")
                or line.startswith("GigabitEthernet")
                or line.startswith("XGigabitEthernet")
                or line.startswith("Vlanif")
                or line.startswith("NULL")
            ):
                current_iface = line
                continue
            v, k = line.split(" ", 1)
            r[current_iface][k.strip()] = v.strip()
        return r

    _IF_TYPES = {"eth": "physical", "vla": "SVI", "tru": "aggregated"}

    @classmethod
    def get_interface_type(cls, name):
        return cls._IF_TYPES.get(name[:3].lower(), "unknown")