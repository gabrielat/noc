.. _metric-scope-ping:

====
Ping
====
.. contents:: On this page
    :local:
    :backlinks: none
    :depth: 1
    :class: singlecol

Ping-related metrics

Data Table
----------
ClickHouse Table: `ping`

+----------------+--------------+------------------------------------------------------------+
|Field           |Type          |Description                                                 |
+----------------+--------------+------------------------------------------------------------+
|date            |Date          |Measurement Date                                            |
+----------------+--------------+------------------------------------------------------------+
|ts              |DateTime      |Measurement Timestamp                                       |
+----------------+--------------+------------------------------------------------------------+
|managed_object  |UInt64        |(Key) Reference to sa.ManagedObject model (bi_id)           |
+----------------+--------------+------------------------------------------------------------+
|path            |Array(String) |Path:                                                       |
|                |              |                                                            |
+----------------+--------------+------------------------------------------------------------+
|attempts        |UInt16        |:ref:`metric-type-ping-attempts`                            |
+----------------+--------------+------------------------------------------------------------+
|rtt             |UInt32        |:ref:`metric-type-ping-rtt`                                 |
+----------------+--------------+------------------------------------------------------------+
