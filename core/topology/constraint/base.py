# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# BaseConstraint class
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.sa.models.managedobject import ManagedObject
from noc.inv.models.interface import Interface


class BaseConstraint(object):
    def __init__(self):
        # type: () -> None
        pass

    def is_valid_neighbor(self, obj):
        # type: (ManagedObject) -> bool
        """
        Check if neighbor is valid neighbor for the path

        :param obj: Managed Object
        :return: True if path can be continued via neighbors
        """
        return True

    def is_valid_interface(self, interface):
        # type: (Interface) -> bool
        """
        Check if interface is valid interface on the path

        :param interface:
        :return:
        """
        return True

    def is_valid_egress(self, interface):
        # type: (Interface) -> bool
        """
        Check if egress interface is valid interface on the path

        :param interface: Interface instance
        :return: True if path can be continued across the interface
        """
        return self.is_valid_interface(interface)

    def is_valid_ingress(self, interface):
        # type: (Interface) -> bool
        """
        Check if ingress interface is valid interface on the path

        :param interface: Interface instance
        :return: True if path can be continued across the interface
        """
        return self.is_valid_interface(interface)

    def __neg__(self):
        # type: (BaseConstraint) -> BaseConstraint
        return NotConstraint(self)

    def __and__(self, other):
        # type: (BaseConstraint) -> BaseConstraint
        return AndConstraint(self, other)

    def __or__(self, other):
        # type: (BaseConstraint) -> BaseConstraint
        return OrConstraint(self, other)


class AndConstraint(BaseConstraint):
    def __init__(self, left, right):
        # type: (BaseConstraint, BaseConstraint) -> None
        super(AndConstraint, self).__init__()
        self.left = left
        self.right = right

    def is_valid_neighbor(self, obj):
        # type: (ManagedObject) -> bool
        return self.left.is_valid_neighbor(obj) and self.right.is_valid_neighbor(obj)

    def is_valid_interface(self, interface):
        # type: (Interface) -> bool
        return self.left.is_valid_interface(interface) and self.right.is_valid_interface(interface)

    def is_valid_ingress(self, interface):
        # type: (Interface) -> bool
        return self.left.is_valid_ingress(interface) and self.right.is_valid_ingress(interface)

    def is_valid_egress(self, interface):
        # type: (Interface) -> bool
        return self.left.is_valid_egress(interface) and self.right.is_valid_egress(interface)


class OrConstraint(BaseConstraint):
    def __init__(self, left, right):
        # type: (BaseConstraint, BaseConstraint) -> None
        super(OrConstraint, self).__init__()
        self.left = left
        self.right = right

    def is_valid_neighbor(self, obj):
        # type: (ManagedObject) -> bool
        return self.left.is_valid_neighbor(obj) or self.right.is_valid_neighbor(obj)

    def is_valid_interface(self, interface):
        # type: (Interface) -> bool
        return self.left.is_valid_interface(interface) or self.right.is_valid_interface(interface)

    def is_valid_ingress(self, interface):
        # type: (Interface) -> bool
        return self.left.is_valid_ingress(interface) or self.right.is_valid_ingress(interface)

    def is_valid_egress(self, interface):
        # type: (Interface) -> bool
        return self.left.is_valid_egress(interface) or self.right.is_valid_egress(interface)


class NotConstraint(BaseConstraint):
    def __init__(self, constraint):
        # type: (BaseConstraint) -> None
        super(NotConstraint, self).__init__()
        self.constraint = constraint

    def is_valid_neighbor(self, obj):
        # type: (ManagedObject) -> bool
        return not self.constraint.is_valid_neighbor(obj)

    def is_valid_interface(self, interface):
        # type: (Interface) -> bool
        return not self.constraint.is_valid_interface(interface)

    def is_valid_ingress(self, interface):
        # type: (Interface) -> bool
        return not self.constraint.is_valid_ingress(interface)

    def is_valid_egress(self, interface):
        # type: (Interface) -> bool
        return not self.constraint.is_valid_egress(interface)
