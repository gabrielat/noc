## -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Solutions utilities
##----------------------------------------------------------------------
## Copyright (C) 2007-2014 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Django modules
from django.core import exceptions
from django.utils.importlib import import_module
## NOC modules
from noc.settings import config


_CCACHE = {}  # path -> callable

def get_solution(path):
    """
    Returns callable referenced by path
    """
    if path in _CCACHE:
        return _CCACHE[path]
    try:
        m, c = path.rsplit(".", 1)
    except ValueError:
        raise exceptions.ImproperlyConfigured("%s isn't valid solution name" % path)
    try:
        mod = import_module(m)
    except ImportError, e:
        raise exceptions.ImproperlyConfigured("Error loading solution '%s': %s" % (path, e))
    try:
        c = getattr(mod, c)
    except AttributeError:
        raise exceptions.ImproperlyConfigured("Solution '%s' doesn't define '%s' callable" % (path, c))
    _CCACHE[path] = c
    return c


def init_solutions():
    """
    Initialize solutions and load modules
    """
    from noc.main.models import CustomField
    CustomField.install_fields()
    for sn in config.options("solutions"):
        if config.getboolean("solutions", sn):
            load_solution(sn)


def load_solution(name):
    """
    Load and initialize solution by name
    """
    __import__("noc.solutions.%s" % name, {}, {}, "")
