# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# IConfigValidator
# ---------------------------------------------------------------------
# Copyright (C) 2007-2011 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# NOC modules
from noc.core.interface.base import BaseInterface
from .base import InstanceOfParameter, StringParameter, StringListParameter


class IConfigValidator(BaseInterface):
    managed_object = InstanceOfParameter("ManagedObject")
    config = StringParameter()
    returns = StringListParameter()
