# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# LLDP-MIB
# Compiled MIB
# Do not modify this file directly
# Run ./noc mib make-cmib instead
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# MIB Name
NAME = "LLDP-MIB"

# Metadata
LAST_UPDATED = "2005-05-06"
COMPILED = "2020-01-19"

# MIB Data: name -> oid
MIB = {
    "LLDP-MIB::lldpMIB": "1.0.8802.1.1.2",
    "LLDP-MIB::lldpNotifications": "1.0.8802.1.1.2.0",
    "LLDP-MIB::lldpNotificationPrefix": "1.0.8802.1.1.2.0.0",
    "LLDP-MIB::lldpRemTablesChange": "1.0.8802.1.1.2.0.0.1",
    "LLDP-MIB::lldpObjects": "1.0.8802.1.1.2.1",
    "LLDP-MIB::lldpConfiguration": "1.0.8802.1.1.2.1.1",
    "LLDP-MIB::lldpMessageTxInterval": "1.0.8802.1.1.2.1.1.1",
    "LLDP-MIB::lldpMessageTxHoldMultiplier": "1.0.8802.1.1.2.1.1.2",
    "LLDP-MIB::lldpReinitDelay": "1.0.8802.1.1.2.1.1.3",
    "LLDP-MIB::lldpTxDelay": "1.0.8802.1.1.2.1.1.4",
    "LLDP-MIB::lldpNotificationInterval": "1.0.8802.1.1.2.1.1.5",
    "LLDP-MIB::lldpPortConfigTable": "1.0.8802.1.1.2.1.1.6",
    "LLDP-MIB::lldpPortConfigEntry": "1.0.8802.1.1.2.1.1.6.1",
    "LLDP-MIB::lldpPortConfigPortNum": "1.0.8802.1.1.2.1.1.6.1.1",
    "LLDP-MIB::lldpPortConfigAdminStatus": "1.0.8802.1.1.2.1.1.6.1.2",
    "LLDP-MIB::lldpPortConfigNotificationEnable": "1.0.8802.1.1.2.1.1.6.1.3",
    "LLDP-MIB::lldpPortConfigTLVsTxEnable": "1.0.8802.1.1.2.1.1.6.1.4",
    "LLDP-MIB::lldpConfigManAddrTable": "1.0.8802.1.1.2.1.1.7",
    "LLDP-MIB::lldpConfigManAddrEntry": "1.0.8802.1.1.2.1.1.7.1",
    "LLDP-MIB::lldpConfigManAddrPortsTxEnable": "1.0.8802.1.1.2.1.1.7.1.1",
    "LLDP-MIB::lldpStatistics": "1.0.8802.1.1.2.1.2",
    "LLDP-MIB::lldpStatsRemTablesLastChangeTime": "1.0.8802.1.1.2.1.2.1",
    "LLDP-MIB::lldpStatsRemTablesInserts": "1.0.8802.1.1.2.1.2.2",
    "LLDP-MIB::lldpStatsRemTablesDeletes": "1.0.8802.1.1.2.1.2.3",
    "LLDP-MIB::lldpStatsRemTablesDrops": "1.0.8802.1.1.2.1.2.4",
    "LLDP-MIB::lldpStatsRemTablesAgeouts": "1.0.8802.1.1.2.1.2.5",
    "LLDP-MIB::lldpStatsTxPortTable": "1.0.8802.1.1.2.1.2.6",
    "LLDP-MIB::lldpStatsTxPortEntry": "1.0.8802.1.1.2.1.2.6.1",
    "LLDP-MIB::lldpStatsTxPortNum": "1.0.8802.1.1.2.1.2.6.1.1",
    "LLDP-MIB::lldpStatsTxPortFramesTotal": "1.0.8802.1.1.2.1.2.6.1.2",
    "LLDP-MIB::lldpStatsRxPortTable": "1.0.8802.1.1.2.1.2.7",
    "LLDP-MIB::lldpStatsRxPortEntry": "1.0.8802.1.1.2.1.2.7.1",
    "LLDP-MIB::lldpStatsRxPortNum": "1.0.8802.1.1.2.1.2.7.1.1",
    "LLDP-MIB::lldpStatsRxPortFramesDiscardedTotal": "1.0.8802.1.1.2.1.2.7.1.2",
    "LLDP-MIB::lldpStatsRxPortFramesErrors": "1.0.8802.1.1.2.1.2.7.1.3",
    "LLDP-MIB::lldpStatsRxPortFramesTotal": "1.0.8802.1.1.2.1.2.7.1.4",
    "LLDP-MIB::lldpStatsRxPortTLVsDiscardedTotal": "1.0.8802.1.1.2.1.2.7.1.5",
    "LLDP-MIB::lldpStatsRxPortTLVsUnrecognizedTotal": "1.0.8802.1.1.2.1.2.7.1.6",
    "LLDP-MIB::lldpStatsRxPortAgeoutsTotal": "1.0.8802.1.1.2.1.2.7.1.7",
    "LLDP-MIB::lldpLocalSystemData": "1.0.8802.1.1.2.1.3",
    "LLDP-MIB::lldpLocChassisIdSubtype": "1.0.8802.1.1.2.1.3.1",
    "LLDP-MIB::lldpLocChassisId": "1.0.8802.1.1.2.1.3.2",
    "LLDP-MIB::lldpLocSysName": "1.0.8802.1.1.2.1.3.3",
    "LLDP-MIB::lldpLocSysDesc": "1.0.8802.1.1.2.1.3.4",
    "LLDP-MIB::lldpLocSysCapSupported": "1.0.8802.1.1.2.1.3.5",
    "LLDP-MIB::lldpLocSysCapEnabled": "1.0.8802.1.1.2.1.3.6",
    "LLDP-MIB::lldpLocPortTable": "1.0.8802.1.1.2.1.3.7",
    "LLDP-MIB::lldpLocPortEntry": "1.0.8802.1.1.2.1.3.7.1",
    "LLDP-MIB::lldpLocPortNum": "1.0.8802.1.1.2.1.3.7.1.1",
    "LLDP-MIB::lldpLocPortIdSubtype": "1.0.8802.1.1.2.1.3.7.1.2",
    "LLDP-MIB::lldpLocPortId": "1.0.8802.1.1.2.1.3.7.1.3",
    "LLDP-MIB::lldpLocPortDesc": "1.0.8802.1.1.2.1.3.7.1.4",
    "LLDP-MIB::lldpLocManAddrTable": "1.0.8802.1.1.2.1.3.8",
    "LLDP-MIB::lldpLocManAddrEntry": "1.0.8802.1.1.2.1.3.8.1",
    "LLDP-MIB::lldpLocManAddrSubtype": "1.0.8802.1.1.2.1.3.8.1.1",
    "LLDP-MIB::lldpLocManAddr": "1.0.8802.1.1.2.1.3.8.1.2",
    "LLDP-MIB::lldpLocManAddrLen": "1.0.8802.1.1.2.1.3.8.1.3",
    "LLDP-MIB::lldpLocManAddrIfSubtype": "1.0.8802.1.1.2.1.3.8.1.4",
    "LLDP-MIB::lldpLocManAddrIfId": "1.0.8802.1.1.2.1.3.8.1.5",
    "LLDP-MIB::lldpLocManAddrOID": "1.0.8802.1.1.2.1.3.8.1.6",
    "LLDP-MIB::lldpRemoteSystemsData": "1.0.8802.1.1.2.1.4",
    "LLDP-MIB::lldpRemTable": "1.0.8802.1.1.2.1.4.1",
    "LLDP-MIB::lldpRemEntry": "1.0.8802.1.1.2.1.4.1.1",
    "LLDP-MIB::lldpRemTimeMark": "1.0.8802.1.1.2.1.4.1.1.1",
    "LLDP-MIB::lldpRemLocalPortNum": "1.0.8802.1.1.2.1.4.1.1.2",
    "LLDP-MIB::lldpRemIndex": "1.0.8802.1.1.2.1.4.1.1.3",
    "LLDP-MIB::lldpRemChassisIdSubtype": "1.0.8802.1.1.2.1.4.1.1.4",
    "LLDP-MIB::lldpRemChassisId": "1.0.8802.1.1.2.1.4.1.1.5",
    "LLDP-MIB::lldpRemPortIdSubtype": "1.0.8802.1.1.2.1.4.1.1.6",
    "LLDP-MIB::lldpRemPortId": "1.0.8802.1.1.2.1.4.1.1.7",
    "LLDP-MIB::lldpRemPortDesc": "1.0.8802.1.1.2.1.4.1.1.8",
    "LLDP-MIB::lldpRemSysName": "1.0.8802.1.1.2.1.4.1.1.9",
    "LLDP-MIB::lldpRemSysDesc": "1.0.8802.1.1.2.1.4.1.1.10",
    "LLDP-MIB::lldpRemSysCapSupported": "1.0.8802.1.1.2.1.4.1.1.11",
    "LLDP-MIB::lldpRemSysCapEnabled": "1.0.8802.1.1.2.1.4.1.1.12",
    "LLDP-MIB::lldpRemManAddrTable": "1.0.8802.1.1.2.1.4.2",
    "LLDP-MIB::lldpRemManAddrEntry": "1.0.8802.1.1.2.1.4.2.1",
    "LLDP-MIB::lldpRemManAddrSubtype": "1.0.8802.1.1.2.1.4.2.1.1",
    "LLDP-MIB::lldpRemManAddr": "1.0.8802.1.1.2.1.4.2.1.2",
    "LLDP-MIB::lldpRemManAddrIfSubtype": "1.0.8802.1.1.2.1.4.2.1.3",
    "LLDP-MIB::lldpRemManAddrIfId": "1.0.8802.1.1.2.1.4.2.1.4",
    "LLDP-MIB::lldpRemManAddrOID": "1.0.8802.1.1.2.1.4.2.1.5",
    "LLDP-MIB::lldpRemUnknownTLVTable": "1.0.8802.1.1.2.1.4.3",
    "LLDP-MIB::lldpRemUnknownTLVEntry": "1.0.8802.1.1.2.1.4.3.1",
    "LLDP-MIB::lldpRemUnknownTLVType": "1.0.8802.1.1.2.1.4.3.1.1",
    "LLDP-MIB::lldpRemUnknownTLVInfo": "1.0.8802.1.1.2.1.4.3.1.2",
    "LLDP-MIB::lldpRemOrgDefInfoTable": "1.0.8802.1.1.2.1.4.4",
    "LLDP-MIB::lldpRemOrgDefInfoEntry": "1.0.8802.1.1.2.1.4.4.1",
    "LLDP-MIB::lldpRemOrgDefInfoOUI": "1.0.8802.1.1.2.1.4.4.1.1",
    "LLDP-MIB::lldpRemOrgDefInfoSubtype": "1.0.8802.1.1.2.1.4.4.1.2",
    "LLDP-MIB::lldpRemOrgDefInfoIndex": "1.0.8802.1.1.2.1.4.4.1.3",
    "LLDP-MIB::lldpRemOrgDefInfo": "1.0.8802.1.1.2.1.4.4.1.4",
    "LLDP-MIB::lldpExtensions": "1.0.8802.1.1.2.1.5",
    "LLDP-MIB::lldpConformance": "1.0.8802.1.1.2.2",
    "LLDP-MIB::lldpCompliances": "1.0.8802.1.1.2.2.1",
    "LLDP-MIB::lldpGroups": "1.0.8802.1.1.2.2.2",
}

DISPLAY_HINTS = {}
