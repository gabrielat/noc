# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# MPLS-L3VPN-STD-MIB
# Compiled MIB
# Do not modify this file directly
# Run ./noc mib make-cmib instead
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# MIB Name
NAME = "MPLS-L3VPN-STD-MIB"

# Metadata
LAST_UPDATED = "2006-01-23"
COMPILED = "2020-01-19"

# MIB Data: name -> oid
MIB = {
    "MPLS-L3VPN-STD-MIB::mplsL3VpnMIB": "1.3.6.1.2.1.10.166.11",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnNotifications": "1.3.6.1.2.1.10.166.11.0",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfUp": "1.3.6.1.2.1.10.166.11.0.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfDown": "1.3.6.1.2.1.10.166.11.0.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRouteMidThreshExceeded": "1.3.6.1.2.1.10.166.11.0.3",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfNumVrfRouteMaxThreshExceeded": "1.3.6.1.2.1.10.166.11.0.4",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnNumVrfSecIllglLblThrshExcd": "1.3.6.1.2.1.10.166.11.0.5",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnNumVrfRouteMaxThreshCleared": "1.3.6.1.2.1.10.166.11.0.6",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnObjects": "1.3.6.1.2.1.10.166.11.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnScalars": "1.3.6.1.2.1.10.166.11.1.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnConfiguredVrfs": "1.3.6.1.2.1.10.166.11.1.1.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnActiveVrfs": "1.3.6.1.2.1.10.166.11.1.1.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnConnectedInterfaces": "1.3.6.1.2.1.10.166.11.1.1.3",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnNotificationEnable": "1.3.6.1.2.1.10.166.11.1.1.4",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfConfMaxPossRts": "1.3.6.1.2.1.10.166.11.1.1.5",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfConfRteMxThrshTime": "1.3.6.1.2.1.10.166.11.1.1.6",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnIllLblRcvThrsh": "1.3.6.1.2.1.10.166.11.1.1.7",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnConf": "1.3.6.1.2.1.10.166.11.1.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnIfConfTable": "1.3.6.1.2.1.10.166.11.1.2.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnIfConfEntry": "1.3.6.1.2.1.10.166.11.1.2.1.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnIfConfIndex": "1.3.6.1.2.1.10.166.11.1.2.1.1.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnIfVpnClassification": "1.3.6.1.2.1.10.166.11.1.2.1.1.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnIfVpnRouteDistProtocol": "1.3.6.1.2.1.10.166.11.1.2.1.1.3",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnIfConfStorageType": "1.3.6.1.2.1.10.166.11.1.2.1.1.4",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnIfConfRowStatus": "1.3.6.1.2.1.10.166.11.1.2.1.1.5",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfTable": "1.3.6.1.2.1.10.166.11.1.2.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfEntry": "1.3.6.1.2.1.10.166.11.1.2.2.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfName": "1.3.6.1.2.1.10.166.11.1.2.2.1.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfVpnId": "1.3.6.1.2.1.10.166.11.1.2.2.1.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfDescription": "1.3.6.1.2.1.10.166.11.1.2.2.1.3",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRD": "1.3.6.1.2.1.10.166.11.1.2.2.1.4",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfCreationTime": "1.3.6.1.2.1.10.166.11.1.2.2.1.5",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfOperStatus": "1.3.6.1.2.1.10.166.11.1.2.2.1.6",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfActiveInterfaces": "1.3.6.1.2.1.10.166.11.1.2.2.1.7",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfAssociatedInterfaces": "1.3.6.1.2.1.10.166.11.1.2.2.1.8",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfConfMidRteThresh": "1.3.6.1.2.1.10.166.11.1.2.2.1.9",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfConfHighRteThresh": "1.3.6.1.2.1.10.166.11.1.2.2.1.10",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfConfMaxRoutes": "1.3.6.1.2.1.10.166.11.1.2.2.1.11",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfConfLastChanged": "1.3.6.1.2.1.10.166.11.1.2.2.1.12",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfConfRowStatus": "1.3.6.1.2.1.10.166.11.1.2.2.1.13",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfConfAdminStatus": "1.3.6.1.2.1.10.166.11.1.2.2.1.14",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfConfStorageType": "1.3.6.1.2.1.10.166.11.1.2.2.1.15",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRTTable": "1.3.6.1.2.1.10.166.11.1.2.3",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRTEntry": "1.3.6.1.2.1.10.166.11.1.2.3.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRTIndex": "1.3.6.1.2.1.10.166.11.1.2.3.1.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRTType": "1.3.6.1.2.1.10.166.11.1.2.3.1.3",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRT": "1.3.6.1.2.1.10.166.11.1.2.3.1.4",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRTDescr": "1.3.6.1.2.1.10.166.11.1.2.3.1.5",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRTRowStatus": "1.3.6.1.2.1.10.166.11.1.2.3.1.6",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRTStorageType": "1.3.6.1.2.1.10.166.11.1.2.3.1.7",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfSecTable": "1.3.6.1.2.1.10.166.11.1.2.6",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfSecEntry": "1.3.6.1.2.1.10.166.11.1.2.6.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfSecIllegalLblVltns": "1.3.6.1.2.1.10.166.11.1.2.6.1.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfSecDiscontinuityTime": "1.3.6.1.2.1.10.166.11.1.2.6.1.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnPerf": "1.3.6.1.2.1.10.166.11.1.3",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfPerfTable": "1.3.6.1.2.1.10.166.11.1.3.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfPerfEntry": "1.3.6.1.2.1.10.166.11.1.3.1.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfPerfRoutesAdded": "1.3.6.1.2.1.10.166.11.1.3.1.1.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfPerfRoutesDeleted": "1.3.6.1.2.1.10.166.11.1.3.1.1.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfPerfCurrNumRoutes": "1.3.6.1.2.1.10.166.11.1.3.1.1.3",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfPerfRoutesDropped": "1.3.6.1.2.1.10.166.11.1.3.1.1.4",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfPerfDiscTime": "1.3.6.1.2.1.10.166.11.1.3.1.1.5",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnRoute": "1.3.6.1.2.1.10.166.11.1.4",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteTable": "1.3.6.1.2.1.10.166.11.1.4.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteEntry": "1.3.6.1.2.1.10.166.11.1.4.1.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrDestType": "1.3.6.1.2.1.10.166.11.1.4.1.1.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrDest": "1.3.6.1.2.1.10.166.11.1.4.1.1.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrPfxLen": "1.3.6.1.2.1.10.166.11.1.4.1.1.3",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrPolicy": "1.3.6.1.2.1.10.166.11.1.4.1.1.4",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrNHopType": "1.3.6.1.2.1.10.166.11.1.4.1.1.5",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrNextHop": "1.3.6.1.2.1.10.166.11.1.4.1.1.6",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrIfIndex": "1.3.6.1.2.1.10.166.11.1.4.1.1.7",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrType": "1.3.6.1.2.1.10.166.11.1.4.1.1.8",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrProto": "1.3.6.1.2.1.10.166.11.1.4.1.1.9",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrAge": "1.3.6.1.2.1.10.166.11.1.4.1.1.10",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrNextHopAS": "1.3.6.1.2.1.10.166.11.1.4.1.1.11",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrMetric1": "1.3.6.1.2.1.10.166.11.1.4.1.1.12",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrMetric2": "1.3.6.1.2.1.10.166.11.1.4.1.1.13",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrMetric3": "1.3.6.1.2.1.10.166.11.1.4.1.1.14",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrMetric4": "1.3.6.1.2.1.10.166.11.1.4.1.1.15",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrMetric5": "1.3.6.1.2.1.10.166.11.1.4.1.1.16",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteXCPointer": "1.3.6.1.2.1.10.166.11.1.4.1.1.17",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrStatus": "1.3.6.1.2.1.10.166.11.1.4.1.1.18",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnConformance": "1.3.6.1.2.1.10.166.11.2",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnGroups": "1.3.6.1.2.1.10.166.11.2.1",
    "MPLS-L3VPN-STD-MIB::mplsL3VpnCompliances": "1.3.6.1.2.1.10.166.11.2.2",
}

DISPLAY_HINTS = {
    "1.3.6.1.2.1.10.166.11.1.2.2.1.3": ("OctetString", "255t"),  # MPLS-L3VPN-STD-MIB::mplsL3VpnVrfDescription
    "1.3.6.1.2.1.10.166.11.1.2.3.1.5": ("OctetString", "255t"),  # MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRTDescr
    "1.3.6.1.2.1.10.166.11.1.4.1.1.11": ("Unsigned32", "d"),  # MPLS-L3VPN-STD-MIB::mplsL3VpnVrfRteInetCidrNextHopAS
}
