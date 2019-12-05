# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Test ConfDB syntax
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import pytest
import cachetools

# NOC modules
from noc.core.confdb.syntax.base import SYNTAX


@cachetools.cached({})
def get_nodes():
    def iter_children(path):
        yield path
        if path[-1].children:
            for c in path[-1].children:
                for p in iter_children(path + (c,)):
                    yield p

    def iter_nodes():
        for node in SYNTAX:
            for path in iter_children((node,)):
                yield path

    return list(iter_nodes())


def get_path(path):
    def q(n):
        if not isinstance(n.token, type):
            return n.token
        elif n.name:
            return "<%s>" % n.name
        else:
            return "ANY"

    return " ".join(q(p) for p in path)


@pytest.mark.parametrize("nodes", get_nodes(), ids=get_path)
def test_wildcard_names(nodes):
    n = nodes[-1]
    if not n.token:
        assert n.name, "Wildcard without name"
