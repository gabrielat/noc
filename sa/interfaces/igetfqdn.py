# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# IGetFQDN
# ---------------------------------------------------------------------
# Copyright (C) 2007-2010 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# NOC Modules
from noc.core.interface.base import BaseInterface
from .base import StringParameter


class IGetFQDN(BaseInterface):
    returns = StringParameter()
