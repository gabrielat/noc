# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ConfDB hints syntax
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# NOC modules
from .defs import DEF
from .interfaces.hints import INTERFACES_HINTS_SYNTAX
from .protocols.hints import PROTOCOLS_HINTS_SYNTAX

HINTS_SYNTAX = DEF("hints", [INTERFACES_HINTS_SYNTAX, PROTOCOLS_HINTS_SYNTAX])
