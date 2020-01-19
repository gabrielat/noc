# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Q-BRIDGE-MIB
# Compiled MIB
# Do not modify this file directly
# Run ./noc mib make-cmib instead
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# MIB Name
NAME = "Q-BRIDGE-MIB"

# Metadata
LAST_UPDATED = "2006-01-09"
COMPILED = "2020-01-19"

# MIB Data: name -> oid
MIB = {
    "Q-BRIDGE-MIB::qBridgeMIB": "1.3.6.1.2.1.17.7",
    "Q-BRIDGE-MIB::qBridgeMIBObjects": "1.3.6.1.2.1.17.7.1",
    "Q-BRIDGE-MIB::dot1qBase": "1.3.6.1.2.1.17.7.1.1",
    "Q-BRIDGE-MIB::dot1qVlanVersionNumber": "1.3.6.1.2.1.17.7.1.1.1",
    "Q-BRIDGE-MIB::dot1qMaxVlanId": "1.3.6.1.2.1.17.7.1.1.2",
    "Q-BRIDGE-MIB::dot1qMaxSupportedVlans": "1.3.6.1.2.1.17.7.1.1.3",
    "Q-BRIDGE-MIB::dot1qNumVlans": "1.3.6.1.2.1.17.7.1.1.4",
    "Q-BRIDGE-MIB::dot1qGvrpStatus": "1.3.6.1.2.1.17.7.1.1.5",
    "Q-BRIDGE-MIB::dot1qTp": "1.3.6.1.2.1.17.7.1.2",
    "Q-BRIDGE-MIB::dot1qFdbTable": "1.3.6.1.2.1.17.7.1.2.1",
    "Q-BRIDGE-MIB::dot1qFdbEntry": "1.3.6.1.2.1.17.7.1.2.1.1",
    "Q-BRIDGE-MIB::dot1qFdbId": "1.3.6.1.2.1.17.7.1.2.1.1.1",
    "Q-BRIDGE-MIB::dot1qFdbDynamicCount": "1.3.6.1.2.1.17.7.1.2.1.1.2",
    "Q-BRIDGE-MIB::dot1qTpFdbTable": "1.3.6.1.2.1.17.7.1.2.2",
    "Q-BRIDGE-MIB::dot1qTpFdbEntry": "1.3.6.1.2.1.17.7.1.2.2.1",
    "Q-BRIDGE-MIB::dot1qTpFdbAddress": "1.3.6.1.2.1.17.7.1.2.2.1.1",
    "Q-BRIDGE-MIB::dot1qTpFdbPort": "1.3.6.1.2.1.17.7.1.2.2.1.2",
    "Q-BRIDGE-MIB::dot1qTpFdbStatus": "1.3.6.1.2.1.17.7.1.2.2.1.3",
    "Q-BRIDGE-MIB::dot1qTpGroupTable": "1.3.6.1.2.1.17.7.1.2.3",
    "Q-BRIDGE-MIB::dot1qTpGroupEntry": "1.3.6.1.2.1.17.7.1.2.3.1",
    "Q-BRIDGE-MIB::dot1qTpGroupAddress": "1.3.6.1.2.1.17.7.1.2.3.1.1",
    "Q-BRIDGE-MIB::dot1qTpGroupEgressPorts": "1.3.6.1.2.1.17.7.1.2.3.1.2",
    "Q-BRIDGE-MIB::dot1qTpGroupLearnt": "1.3.6.1.2.1.17.7.1.2.3.1.3",
    "Q-BRIDGE-MIB::dot1qForwardAllTable": "1.3.6.1.2.1.17.7.1.2.4",
    "Q-BRIDGE-MIB::dot1qForwardAllEntry": "1.3.6.1.2.1.17.7.1.2.4.1",
    "Q-BRIDGE-MIB::dot1qForwardAllPorts": "1.3.6.1.2.1.17.7.1.2.4.1.1",
    "Q-BRIDGE-MIB::dot1qForwardAllStaticPorts": "1.3.6.1.2.1.17.7.1.2.4.1.2",
    "Q-BRIDGE-MIB::dot1qForwardAllForbiddenPorts": "1.3.6.1.2.1.17.7.1.2.4.1.3",
    "Q-BRIDGE-MIB::dot1qForwardUnregisteredTable": "1.3.6.1.2.1.17.7.1.2.5",
    "Q-BRIDGE-MIB::dot1qForwardUnregisteredEntry": "1.3.6.1.2.1.17.7.1.2.5.1",
    "Q-BRIDGE-MIB::dot1qForwardUnregisteredPorts": "1.3.6.1.2.1.17.7.1.2.5.1.1",
    "Q-BRIDGE-MIB::dot1qForwardUnregisteredStaticPorts": "1.3.6.1.2.1.17.7.1.2.5.1.2",
    "Q-BRIDGE-MIB::dot1qForwardUnregisteredForbiddenPorts": "1.3.6.1.2.1.17.7.1.2.5.1.3",
    "Q-BRIDGE-MIB::dot1qStatic": "1.3.6.1.2.1.17.7.1.3",
    "Q-BRIDGE-MIB::dot1qStaticUnicastTable": "1.3.6.1.2.1.17.7.1.3.1",
    "Q-BRIDGE-MIB::dot1qStaticUnicastEntry": "1.3.6.1.2.1.17.7.1.3.1.1",
    "Q-BRIDGE-MIB::dot1qStaticUnicastAddress": "1.3.6.1.2.1.17.7.1.3.1.1.1",
    "Q-BRIDGE-MIB::dot1qStaticUnicastReceivePort": "1.3.6.1.2.1.17.7.1.3.1.1.2",
    "Q-BRIDGE-MIB::dot1qStaticUnicastAllowedToGoTo": "1.3.6.1.2.1.17.7.1.3.1.1.3",
    "Q-BRIDGE-MIB::dot1qStaticUnicastStatus": "1.3.6.1.2.1.17.7.1.3.1.1.4",
    "Q-BRIDGE-MIB::dot1qStaticMulticastTable": "1.3.6.1.2.1.17.7.1.3.2",
    "Q-BRIDGE-MIB::dot1qStaticMulticastEntry": "1.3.6.1.2.1.17.7.1.3.2.1",
    "Q-BRIDGE-MIB::dot1qStaticMulticastAddress": "1.3.6.1.2.1.17.7.1.3.2.1.1",
    "Q-BRIDGE-MIB::dot1qStaticMulticastReceivePort": "1.3.6.1.2.1.17.7.1.3.2.1.2",
    "Q-BRIDGE-MIB::dot1qStaticMulticastStaticEgressPorts": "1.3.6.1.2.1.17.7.1.3.2.1.3",
    "Q-BRIDGE-MIB::dot1qStaticMulticastForbiddenEgressPorts": "1.3.6.1.2.1.17.7.1.3.2.1.4",
    "Q-BRIDGE-MIB::dot1qStaticMulticastStatus": "1.3.6.1.2.1.17.7.1.3.2.1.5",
    "Q-BRIDGE-MIB::dot1qVlan": "1.3.6.1.2.1.17.7.1.4",
    "Q-BRIDGE-MIB::dot1qVlanNumDeletes": "1.3.6.1.2.1.17.7.1.4.1",
    "Q-BRIDGE-MIB::dot1qVlanCurrentTable": "1.3.6.1.2.1.17.7.1.4.2",
    "Q-BRIDGE-MIB::dot1qVlanCurrentEntry": "1.3.6.1.2.1.17.7.1.4.2.1",
    "Q-BRIDGE-MIB::dot1qVlanTimeMark": "1.3.6.1.2.1.17.7.1.4.2.1.1",
    "Q-BRIDGE-MIB::dot1qVlanIndex": "1.3.6.1.2.1.17.7.1.4.2.1.2",
    "Q-BRIDGE-MIB::dot1qVlanFdbId": "1.3.6.1.2.1.17.7.1.4.2.1.3",
    "Q-BRIDGE-MIB::dot1qVlanCurrentEgressPorts": "1.3.6.1.2.1.17.7.1.4.2.1.4",
    "Q-BRIDGE-MIB::dot1qVlanCurrentUntaggedPorts": "1.3.6.1.2.1.17.7.1.4.2.1.5",
    "Q-BRIDGE-MIB::dot1qVlanStatus": "1.3.6.1.2.1.17.7.1.4.2.1.6",
    "Q-BRIDGE-MIB::dot1qVlanCreationTime": "1.3.6.1.2.1.17.7.1.4.2.1.7",
    "Q-BRIDGE-MIB::dot1qVlanStaticTable": "1.3.6.1.2.1.17.7.1.4.3",
    "Q-BRIDGE-MIB::dot1qVlanStaticEntry": "1.3.6.1.2.1.17.7.1.4.3.1",
    "Q-BRIDGE-MIB::dot1qVlanStaticName": "1.3.6.1.2.1.17.7.1.4.3.1.1",
    "Q-BRIDGE-MIB::dot1qVlanStaticEgressPorts": "1.3.6.1.2.1.17.7.1.4.3.1.2",
    "Q-BRIDGE-MIB::dot1qVlanForbiddenEgressPorts": "1.3.6.1.2.1.17.7.1.4.3.1.3",
    "Q-BRIDGE-MIB::dot1qVlanStaticUntaggedPorts": "1.3.6.1.2.1.17.7.1.4.3.1.4",
    "Q-BRIDGE-MIB::dot1qVlanStaticRowStatus": "1.3.6.1.2.1.17.7.1.4.3.1.5",
    "Q-BRIDGE-MIB::dot1qNextFreeLocalVlanIndex": "1.3.6.1.2.1.17.7.1.4.4",
    "Q-BRIDGE-MIB::dot1qPortVlanTable": "1.3.6.1.2.1.17.7.1.4.5",
    "Q-BRIDGE-MIB::dot1qPortVlanEntry": "1.3.6.1.2.1.17.7.1.4.5.1",
    "Q-BRIDGE-MIB::dot1qPvid": "1.3.6.1.2.1.17.7.1.4.5.1.1",
    "Q-BRIDGE-MIB::dot1qPortAcceptableFrameTypes": "1.3.6.1.2.1.17.7.1.4.5.1.2",
    "Q-BRIDGE-MIB::dot1qPortIngressFiltering": "1.3.6.1.2.1.17.7.1.4.5.1.3",
    "Q-BRIDGE-MIB::dot1qPortGvrpStatus": "1.3.6.1.2.1.17.7.1.4.5.1.4",
    "Q-BRIDGE-MIB::dot1qPortGvrpFailedRegistrations": "1.3.6.1.2.1.17.7.1.4.5.1.5",
    "Q-BRIDGE-MIB::dot1qPortGvrpLastPduOrigin": "1.3.6.1.2.1.17.7.1.4.5.1.6",
    "Q-BRIDGE-MIB::dot1qPortRestrictedVlanRegistration": "1.3.6.1.2.1.17.7.1.4.5.1.7",
    "Q-BRIDGE-MIB::dot1qPortVlanStatisticsTable": "1.3.6.1.2.1.17.7.1.4.6",
    "Q-BRIDGE-MIB::dot1qPortVlanStatisticsEntry": "1.3.6.1.2.1.17.7.1.4.6.1",
    "Q-BRIDGE-MIB::dot1qTpVlanPortInFrames": "1.3.6.1.2.1.17.7.1.4.6.1.1",
    "Q-BRIDGE-MIB::dot1qTpVlanPortOutFrames": "1.3.6.1.2.1.17.7.1.4.6.1.2",
    "Q-BRIDGE-MIB::dot1qTpVlanPortInDiscards": "1.3.6.1.2.1.17.7.1.4.6.1.3",
    "Q-BRIDGE-MIB::dot1qTpVlanPortInOverflowFrames": "1.3.6.1.2.1.17.7.1.4.6.1.4",
    "Q-BRIDGE-MIB::dot1qTpVlanPortOutOverflowFrames": "1.3.6.1.2.1.17.7.1.4.6.1.5",
    "Q-BRIDGE-MIB::dot1qTpVlanPortInOverflowDiscards": "1.3.6.1.2.1.17.7.1.4.6.1.6",
    "Q-BRIDGE-MIB::dot1qPortVlanHCStatisticsTable": "1.3.6.1.2.1.17.7.1.4.7",
    "Q-BRIDGE-MIB::dot1qPortVlanHCStatisticsEntry": "1.3.6.1.2.1.17.7.1.4.7.1",
    "Q-BRIDGE-MIB::dot1qTpVlanPortHCInFrames": "1.3.6.1.2.1.17.7.1.4.7.1.1",
    "Q-BRIDGE-MIB::dot1qTpVlanPortHCOutFrames": "1.3.6.1.2.1.17.7.1.4.7.1.2",
    "Q-BRIDGE-MIB::dot1qTpVlanPortHCInDiscards": "1.3.6.1.2.1.17.7.1.4.7.1.3",
    "Q-BRIDGE-MIB::dot1qLearningConstraintsTable": "1.3.6.1.2.1.17.7.1.4.8",
    "Q-BRIDGE-MIB::dot1qLearningConstraintsEntry": "1.3.6.1.2.1.17.7.1.4.8.1",
    "Q-BRIDGE-MIB::dot1qConstraintVlan": "1.3.6.1.2.1.17.7.1.4.8.1.1",
    "Q-BRIDGE-MIB::dot1qConstraintSet": "1.3.6.1.2.1.17.7.1.4.8.1.2",
    "Q-BRIDGE-MIB::dot1qConstraintType": "1.3.6.1.2.1.17.7.1.4.8.1.3",
    "Q-BRIDGE-MIB::dot1qConstraintStatus": "1.3.6.1.2.1.17.7.1.4.8.1.4",
    "Q-BRIDGE-MIB::dot1qConstraintSetDefault": "1.3.6.1.2.1.17.7.1.4.9",
    "Q-BRIDGE-MIB::dot1qConstraintTypeDefault": "1.3.6.1.2.1.17.7.1.4.10",
    "Q-BRIDGE-MIB::dot1vProtocol": "1.3.6.1.2.1.17.7.1.5",
    "Q-BRIDGE-MIB::dot1vProtocolGroupTable": "1.3.6.1.2.1.17.7.1.5.1",
    "Q-BRIDGE-MIB::dot1vProtocolGroupEntry": "1.3.6.1.2.1.17.7.1.5.1.1",
    "Q-BRIDGE-MIB::dot1vProtocolTemplateFrameType": "1.3.6.1.2.1.17.7.1.5.1.1.1",
    "Q-BRIDGE-MIB::dot1vProtocolTemplateProtocolValue": "1.3.6.1.2.1.17.7.1.5.1.1.2",
    "Q-BRIDGE-MIB::dot1vProtocolGroupId": "1.3.6.1.2.1.17.7.1.5.1.1.3",
    "Q-BRIDGE-MIB::dot1vProtocolGroupRowStatus": "1.3.6.1.2.1.17.7.1.5.1.1.4",
    "Q-BRIDGE-MIB::dot1vProtocolPortTable": "1.3.6.1.2.1.17.7.1.5.2",
    "Q-BRIDGE-MIB::dot1vProtocolPortEntry": "1.3.6.1.2.1.17.7.1.5.2.1",
    "Q-BRIDGE-MIB::dot1vProtocolPortGroupId": "1.3.6.1.2.1.17.7.1.5.2.1.1",
    "Q-BRIDGE-MIB::dot1vProtocolPortGroupVid": "1.3.6.1.2.1.17.7.1.5.2.1.2",
    "Q-BRIDGE-MIB::dot1vProtocolPortRowStatus": "1.3.6.1.2.1.17.7.1.5.2.1.3",
    "Q-BRIDGE-MIB::qBridgeConformance": "1.3.6.1.2.1.17.7.2",
    "Q-BRIDGE-MIB::qBridgeGroups": "1.3.6.1.2.1.17.7.2.1",
    "Q-BRIDGE-MIB::qBridgeCompliances": "1.3.6.1.2.1.17.7.2.2",
}

DISPLAY_HINTS = {
    "1.3.6.1.2.1.17.7.1.2.2.1.1": ("OctetString", "1x:"),  # Q-BRIDGE-MIB::dot1qTpFdbAddress
    "1.3.6.1.2.1.17.7.1.2.3.1.1": ("OctetString", "1x:"),  # Q-BRIDGE-MIB::dot1qTpGroupAddress
    "1.3.6.1.2.1.17.7.1.3.1.1.1": ("OctetString", "1x:"),  # Q-BRIDGE-MIB::dot1qStaticUnicastAddress
    "1.3.6.1.2.1.17.7.1.3.2.1.1": ("OctetString", "1x:"),  # Q-BRIDGE-MIB::dot1qStaticMulticastAddress
    "1.3.6.1.2.1.17.7.1.4.2.1.2": ("Unsigned32", "d"),  # Q-BRIDGE-MIB::dot1qVlanIndex
    "1.3.6.1.2.1.17.7.1.4.5.1.1": ("Unsigned32", "d"),  # Q-BRIDGE-MIB::dot1qPvid
    "1.3.6.1.2.1.17.7.1.4.5.1.6": ("OctetString", "1x:"),  # Q-BRIDGE-MIB::dot1qPortGvrpLastPduOrigin
    "1.3.6.1.2.1.17.7.1.4.8.1.1": ("Unsigned32", "d"),  # Q-BRIDGE-MIB::dot1qConstraintVlan
}
