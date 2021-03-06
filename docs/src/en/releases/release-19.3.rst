.. _release-19.3:

========
NOC 19.3
========

In accordance to our :ref:`Release Policy <releases-policy>`
`we're <https://getnoc.com/devteam/>`_ proudly present release `19.3 <https://code.getnoc.com/noc/noc/tags/19.3>`_.

19.3 release contains
`318 <https://code.getnoc.com/noc/noc/merge_requests?scope=all&state=merged&milestone_title=19.3>`_
bugfixes, optimisations and improvements.

Highlights
----------

New Profiles
^^^^^^^^^^^^
* :ref:`Extreme.Summit200<profile-Extreme.Summit200>`
* :ref:`Polygon.IOS<profile-Polygon.IOS>`
* :ref:`Eltex.WOP<profile-Eltex.WOP>`

ConfDB Object and Interface Validation Policies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
NOC 19.3 brings ability to validate object and interface settings
using :ref:`ConfDB Queries<dev-confdb-query>`. This feature
will became primary way of validation and will replace old
CLIPS-based implementation in NOC 19.5.

It is good time to begin legacy validation policy migrations.

ConfDB Syntax Expansion
^^^^^^^^^^^^^^^^^^^^^^^
ConfDB got additional syntax for:

* NTP support
* Video, Audio settings and media streaming

ConfDB 'raw' Section
^^^^^^^^^^^^^^^^^^^^
Raw tokenized input can be applied to ConfDB under the `raw` node.
So platform-depended syntax can be processed via ConfDB Queries and
validators natively, even if no platform-independent syntax exists.
`raw` section may be enabled on Managed Object Profile level.

ConfDB 'meta' Section
^^^^^^^^^^^^^^^^^^^^^
NOC 19.3 adds `meta` section, containing valuable NOC database
information directly exposed to ConfDB queries. Lots of additional
information included:

* Vendor
* Platform
* Software Version
* Profile
* Administrative Domain
* Network Segment
* Managed Object Tags
* Managed Object Profile
* Interface Profile
* Interface Network Neighbors (i.e. Links)

ConfDB Normalizers
^^^^^^^^^^^^^^^^^^
NOC 19.3 introduces 4 new profiles:

* :ref:`Beward.BD<profile-Beward.BD>`
* :ref:`Cisco.IOS<profile-Cisco.IOS>`
* :ref:`Dahua.DH<profile-Dahua.DH>`
* :ref:`Hikvision.DSKV8<profile-Hikvision.DSKV8>`

Uplink Policy
^^^^^^^^^^^^^
Uplink detection algorithm for RCA became configurable now.
Following policies may be used:

* Segment Hierarchy (previous algorithm)
* Object Level
* All Segment Objects
* Lesser Management Address
* Greater Management Address

Uplink policies may be configured at Network Segment Profile level.
Multiple policies may be used with falling back to next policy until
uplinks are detected.

Uplink policies are greatly improve the quality of topology-based RCA.
See :ref:`Uplink Policy<reference-network-segment-profile-uplink-policy>`
for details.

.. _release-19.3-rca-neighbor-cache:

Topology RCA Optimization
^^^^^^^^^^^^^^^^^^^^^^^^^
Topology-based Root-Cause analysis may be resource consumption.
NOC 19.3 introduces new experimental accelerated mode
called `RCA Neighbor Cache`. Smarter data precalculation and caching
in combination of database query optimization and bulk updates
allows to achieve 2-3 times speedup on real-world installations.

To enable the feature perform following steps:

* Run fix::

   $ noc fix apply fix_object_uplinks

* Stop :ref:`services-correlator` processes
* Enable :ref:`config-fm-enable_rca_neighbor_cache` configuration variable
* Start :ref:`services-correlator` processes

.. warning::

    Alarm processing will be postponed when correlator process is stopped,
    so alarm creation and clearing will be delayed until the correlator
    process will be started again.

Prometheus Histograms
^^^^^^^^^^^^^^^^^^^^^
Prometheus histograms and quantiles may be exported via /metrics endpoint.
Additional metrics may be enabled in config.
See :ref:`metrics section<config-metrics>` for details.

ObjectModel Tags
^^^^^^^^^^^^^^^^
Inventory models got additional marking, which may be useful in various cases.
See :ref:`ObjectModel Tags<dev-objectmodel-tags>` for details.
Model's tags are also exposed into :ref:`managedobject DataStream<api-datastream-managedobject>`.

Django upgrade
^^^^^^^^^^^^^^
Previous releases of NOC relied on venerable Django 1.4 dated back to 2012.
Django's team worked hard on improving their product according to their
vision. Unfortunately they tend to introduce a lot of incompatibilities and
upgrading to each next Django\'s major release is the real pain.
Django 1.4 fits our needs well but is not maintained and is incompatible
with Python 3. So it is the time to to collect the pains.

We'd migrated from 1.4 to `1.5 <https://docs.djangoproject.com/en/2.2/releases/1.5/>`_,
then from 1.5 to `1.6 <https://docs.djangoproject.com/en/2.2/releases/1.6/>`_,
then followed by upgrades to `1.7 <https://docs.djangoproject.com/en/2.2/releases/1.7/>`_,
`1.8 <https://docs.djangoproject.com/en/2.2/releases/1.8/>`_,
`1.9 <https://docs.djangoproject.com/en/2.2/releases/1.9/>`_,
`1.10 <https://docs.djangoproject.com/en/2.2/releases/1.10/>`_
and stopped at `1.11 <https://docs.djangoproject.com/en/2.2/releases/1.11/>`_.
During our stroll we'd became very disappointed by Django\'s API stability
and the high maintenance costs for the complex applications and applied
some countermeasures.

NOC 19.3 brings following changes:

* Django 1.11.22
* Django\'s auth contrib package has been replaced with :ref:`AAA module<release-19.3-aaa>`.
* `South` migrations has been replaced with our own :ref:`Migration Engine<release-19.3-migrations>`.
* All legacy Django admin applications (ModelApplication) has been replaced with ExtJS implementations.
* Django will never create or modify database structure on its own (so-called syncdb).
* Django static media repacked as `django-media<https://code.getnoc.com/npkg/django-media>` npkg package.

.. _release-19.3-aaa:

AAA module
^^^^^^^^^^
User and Groups use NOC's own implementation instead of Django\'s ones.
Besides the native ExtJS UI it allows future independent development
according our needs. User Profile became the part of User model.

.. _release-19.3-migrations:

Migration Engine
^^^^^^^^^^^^^^^^
`South <https://south.readthedocs.io/en/latest/>`_ database
migration engine stopped in development and users are urged to
move to Django's 1.7 built-in migration engine. During our investigations
we'd found that we need to completely rewrite 500+ of existing migrations,
migrations code will be bloated by the unnecessary abstractions and we
need to invite the way to preserve old migration history.

So we'd developed migration engine, simple but powerful. Key benefits are:

* Small, clean API.
* Semi-automatical translation of existing migration.
* Seamless migration history conversion.
* Skipped migrations with from other development branch, may be applied later.

Development Process Changes
---------------------------

Code Formatting
^^^^^^^^^^^^^^^

NOC adopts `black <https://black.readthedocs.io/en/stable/>`_ -
the python code formatter. CI pipeline checks code formatting
of changed python files. Any misformatting considered the error
and CI pipeline fails at the `lint` stage. We recommend to
add black formatting to git's pre-commit hook or to the IDE's on-save
hook.

We'd already reformatted all ours codebase and NOC is now fully
`PEP8 <https://www.python.org/dev/peps/pep-0008/>`_-compatible.
Docker container is also available. Use::

    docker run --rm \
        -w /src \
        -v $PWD:/src \
        registry.getnoc.com/infrastructure/black:master \
        /usr/local/bin/black <file name>

to format file

Towards Python 3 compatibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python 3 compatibility became one of our priorities. With 19.3 we'd
fixed lots of incompatibilities, upgraded same dependencies
and becoming to get rid of unsupported ones.
Though a lots of work and testing still required
we're expecting to reach full Python 3 compatibility
in one of future releases.

MR Labels
^^^^^^^^^
We're developed :ref:`the policy<dev-mr-labels>` for Merge Request's (MR) labels.
CI pipeline checks the labels and fails at the `lint` stage in case of errors.
Label policy helps to organize testing and code reviewing process
and quickly explains the goals of MR and subsystems affected.

Breaking Changes
----------------

.. _release-19.3-explicit-mongo-connect:

Explicit MongoDB Connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prior to 19.3 NOC relied that importing of `noc.lib.nosql` automatically
creates MongoDB connection. This kind of auto-magic used to work
but requires to access all mongo-related stuff via `noc.lib.nosql`.
Starting from 19.3 we're beginning to cleanup API and the code and demand,
that MongoDB connection is to be initialized implicitly.

For custom commands and python scripts

.. code-block:: python

    from noc.core.mongo.connection import connect

    ...
    connect()


For custom services set service's `use_mongo` property to `True`

Other Changes
^^^^^^^^^^^^^
* ManagedObjectSelector.resolve_expression() renamed
  to ManagedObjectSelector.get_objects_from_expression()

New features
------------
+------------+---------------------------------------------------------+
| MR         | Title                                                   |
+------------+---------------------------------------------------------+
| :mr:`1682` | ClickHouse LowCardinality support                       |
+------------+---------------------------------------------------------+
| :mr:`2091` | New migrations framework                                |
+------------+---------------------------------------------------------+
| :mr:`2098` | Migration loader, planner and tests                     |
+------------+---------------------------------------------------------+
| :mr:`2179` | Prometheus histograms                                   |
+------------+---------------------------------------------------------+
| :mr:`2181` | ObjectModels tags field                                 |
+------------+---------------------------------------------------------+
| :mr:`2190` | RCA neighbor cache and accelerated topology correlation |
+------------+---------------------------------------------------------+
| :mr:`2220` | Merge UserProfile into User model                       |
+------------+---------------------------------------------------------+
| :mr:`2228` | Platform tags                                           |
+------------+---------------------------------------------------------+
| :mr:`2245` | ./noc test --idea-bookmarks option                      |
+------------+---------------------------------------------------------+
| :mr:`2285` | Uplink Policy                                           |
+------------+---------------------------------------------------------+
| :mr:`2372` | Add MySQL Extractor                                     |
+------------+---------------------------------------------------------+
| :mr:`2400` | ConfDB: ntp support                                     |
+------------+---------------------------------------------------------+
| :mr:`2418` | #1077 ConfDB raw policy                                 |
+------------+---------------------------------------------------------+
| :mr:`2419` | Add new Profile Eltex.WOPLR                             |
+------------+---------------------------------------------------------+
| :mr:`2420` | ConfDB: media section                                   |
+------------+---------------------------------------------------------+
| :mr:`2426` | ConfDB: Object Validation                               |
+------------+---------------------------------------------------------+
| :mr:`2433` | ConfDB: `meta` section                                  |
+------------+---------------------------------------------------------+
| :mr:`2438` | ConfDB: Interface validation                            |
+------------+---------------------------------------------------------+

Improvements
------------
+------------+--------------------------------------------------------------------------------+
| MR         | Title                                                                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`1888` | Django 1.5                                                                     |
+------------+--------------------------------------------------------------------------------+
| :mr:`1965` | Add input_vlan_map and output_vlan_map fields to ConfDB syntax.                |
+------------+--------------------------------------------------------------------------------+
| :mr:`2006` | noc/noc#1032                                                                   |
+------------+--------------------------------------------------------------------------------+
| :mr:`2020` | Add autowidth column option to ReportLinkDetail.                               |
+------------+--------------------------------------------------------------------------------+
| :mr:`2021` | Add autowidth column to ReportIfacesStatus.                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2023` | Add autowidth column option to ReportAlarmDetail.                              |
+------------+--------------------------------------------------------------------------------+
| :mr:`2039` | Add frozen first row in Detail Report.                                         |
+------------+--------------------------------------------------------------------------------+
| :mr:`2041` | Add subscribers profile filter to AlarmDetail Report.                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`2048` | Add ability to get vlans from bridge on MikroTik.RouterOS                      |
+------------+--------------------------------------------------------------------------------+
| :mr:`2055` | Add ignoring snmp to profile checker.                                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`2065` | ensure-indexes: Create index on fm.Uptime                                      |
+------------+--------------------------------------------------------------------------------+
| :mr:`2078` | add get_mac                                                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2084` | Python3 dk improve                                                             |
+------------+--------------------------------------------------------------------------------+
| :mr:`2087` | Django 1.6                                                                     |
+------------+--------------------------------------------------------------------------------+
| :mr:`2088` | Add Content-Transfer-Encoding header to mailsender.                            |
+------------+--------------------------------------------------------------------------------+
| :mr:`2093` | noc/noc#1008                                                                   |
+------------+--------------------------------------------------------------------------------+
| :mr:`2100` | Add search form from Maintenance                                               |
+------------+--------------------------------------------------------------------------------+
| :mr:`2102` | Allow `-` in git tags                                                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`2105` | User, Group ExtJS version                                                      |
+------------+--------------------------------------------------------------------------------+
| :mr:`2108` | Add QSW-3470-28T-AC platform to Qtech. Switch get_version prefer to SNMP.      |
+------------+--------------------------------------------------------------------------------+
| :mr:`2110` | Django 1.7.11                                                                  |
+------------+--------------------------------------------------------------------------------+
| :mr:`2112` | noc/noc#914 Return first find profile that loader.                             |
+------------+--------------------------------------------------------------------------------+
| :mr:`2115` | Add initial support for Extreme.Summit200 profile                              |
+------------+--------------------------------------------------------------------------------+
| :mr:`2117` | Update apply-pools                                                             |
+------------+--------------------------------------------------------------------------------+
| :mr:`2118` | Add depends on set_bi_id migration.                                            |
+------------+--------------------------------------------------------------------------------+
| :mr:`2122` | copy tags to clipboard                                                         |
+------------+--------------------------------------------------------------------------------+
| :mr:`2125` | Cleanup Qtech.QSW2800.get_chassis_id for matcher use.                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`2132` | Update Angtel.Topaz profile                                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2137` | Add ingnore_errors param to http_get activator method.                         |
+------------+--------------------------------------------------------------------------------+
| :mr:`2138` | Add config policy for IBM NOS                                                  |
+------------+--------------------------------------------------------------------------------+
| :mr:`2139` | Add managed param to clickhouse model meta.                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2142` | new profile - Polygon                                                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`2143` | Get serial number for Cisco ASR1000                                            |
+------------+--------------------------------------------------------------------------------+
| :mr:`2144` | Add noc user to docker container                                               |
+------------+--------------------------------------------------------------------------------+
| :mr:`2150` | Remove index field from clickhouse model.                                      |
+------------+--------------------------------------------------------------------------------+
| :mr:`2152` | HP Comware: platform matching, added getting serial number                     |
+------------+--------------------------------------------------------------------------------+
| :mr:`2155` | Check column type when execute ch-migrate.                                     |
+------------+--------------------------------------------------------------------------------+
| :mr:`2157` | Added check of empty lines in the Object and Segment fields                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2158` | Add get_inventory support for Eltex.MES profile                                |
+------------+--------------------------------------------------------------------------------+
| :mr:`2161` | Move report metric to Report Detail format.                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2162` | Docker with memcache                                                           |
+------------+--------------------------------------------------------------------------------+
| :mr:`2168` | Set noc dir permissions                                                        |
+------------+--------------------------------------------------------------------------------+
| :mr:`2178` | added OID for HP A3600-48-PoE                                                  |
+------------+--------------------------------------------------------------------------------+
| :mr:`2180` | Merge noc-docs to main repo                                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2186` | aaa module                                                                     |
+------------+--------------------------------------------------------------------------------+
| :mr:`2187` | mongoengine 0.18                                                               |
+------------+--------------------------------------------------------------------------------+
| :mr:`2188` | export filename as template `appId_YYYYMMDDHHMMSS.csv`                         |
+------------+--------------------------------------------------------------------------------+
| :mr:`2189` | cachetools 3.1.1                                                               |
+------------+--------------------------------------------------------------------------------+
| :mr:`2192` | tagfield add trigger copy to clipboard                                         |
+------------+--------------------------------------------------------------------------------+
| :mr:`2193` | define environmets                                                             |
+------------+--------------------------------------------------------------------------------+
| :mr:`2194` | new/cm-notify                                                                  |
+------------+--------------------------------------------------------------------------------+
| :mr:`2195` | managedobject layout fix                                                       |
+------------+--------------------------------------------------------------------------------+
| :mr:`2196` | ref book admin ExtJS version                                                   |
+------------+--------------------------------------------------------------------------------+
| :mr:`2197` | docs: API autodocumentation                                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2198` | redirect after success login                                                   |
+------------+--------------------------------------------------------------------------------+
| :mr:`2204` | Add administrative domain field to Report Latest Changes.                      |
+------------+--------------------------------------------------------------------------------+
| :mr:`2206` | Add new Radio Metrics Row for rssi/cinr and rx/tx power metrics                |
+------------+--------------------------------------------------------------------------------+
| :mr:`2207` | Migrate to ComboTree                                                           |
+------------+--------------------------------------------------------------------------------+
| :mr:`2213` | Add image options to script command.                                           |
+------------+--------------------------------------------------------------------------------+
| :mr:`2214` | Add config-violatile to Raisecom.ROS.                                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`2217` | Add remote:deleted tag when managedobject removed from etl.                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2218` | Update Ericsson SEOS Profile                                                   |
+------------+--------------------------------------------------------------------------------+
| :mr:`2219` | Django 1.8                                                                     |
+------------+--------------------------------------------------------------------------------+
| :mr:`2222` | Check MR labels                                                                |
+------------+--------------------------------------------------------------------------------+
| :mr:`2223` | documentation last releases description added                                  |
+------------+--------------------------------------------------------------------------------+
| :mr:`2224` | Mongo test hc                                                                  |
+------------+--------------------------------------------------------------------------------+
| :mr:`2225` | Reorganized vendor and profile documentation                                   |
+------------+--------------------------------------------------------------------------------+
| :mr:`2226` | Add Eltex.MES5448.get_inventory script                                         |
+------------+--------------------------------------------------------------------------------+
| :mr:`2227` | Add Eltex.DSLAM.get_inventory script                                           |
+------------+--------------------------------------------------------------------------------+
| :mr:`2229` | Add Eltex.LTP.get_inventory script                                             |
+------------+--------------------------------------------------------------------------------+
| :mr:`2233` | Add support for unpriveleged prompt for Eltex.MES5448                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`2235` | Django 1.9                                                                     |
+------------+--------------------------------------------------------------------------------+
| :mr:`2240` | Update Eltex.ESR profile                                                       |
+------------+--------------------------------------------------------------------------------+
| :mr:`2244` | Add Eltex.LTE.get_inventory script                                             |
+------------+--------------------------------------------------------------------------------+
| :mr:`2246` | Service.use_mongo options to auto-connect to mongo database                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2249` | Add Eltex.MA4000.get_inventory script                                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`2250` | documentation historical releases description added                            |
+------------+--------------------------------------------------------------------------------+
| :mr:`2252` | Build docs when merging to master                                              |
+------------+--------------------------------------------------------------------------------+
| :mr:`2253` | Replace yapf with black                                                        |
+------------+--------------------------------------------------------------------------------+
| :mr:`2254` | Check changed fields when calculate datastream.                                |
+------------+--------------------------------------------------------------------------------+
| :mr:`2256` | Docs config refactor                                                           |
+------------+--------------------------------------------------------------------------------+
| :mr:`2257` | Django 1.10                                                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2258` | Move tests to tmpfs                                                            |
+------------+--------------------------------------------------------------------------------+
| :mr:`2260` | Add mirror options to gridvcs command.                                         |
+------------+--------------------------------------------------------------------------------+
| :mr:`2261` | Explicit MongoDB database connection                                           |
+------------+--------------------------------------------------------------------------------+
| :mr:`2262` | Django 1.11                                                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2272` | Lower artifacts time                                                           |
+------------+--------------------------------------------------------------------------------+
| :mr:`2273` | flake8: Disable E203 check                                                     |
+------------+--------------------------------------------------------------------------------+
| :mr:`2280` | `bandit` analyzer check                                                        |
+------------+--------------------------------------------------------------------------------+
| :mr:`2282` | Move custom mongoengine fields from noc.lib.nosql to noc.core.mongo.fields     |
+------------+--------------------------------------------------------------------------------+
| :mr:`2284` | caniusepython3 and pylint3k checks                                             |
+------------+--------------------------------------------------------------------------------+
| :mr:`2287` | flake8: black-friendly settings                                                |
+------------+--------------------------------------------------------------------------------+
| :mr:`2288` | Set discovery fatal error of profile do not detect profile on Generic devices. |
+------------+--------------------------------------------------------------------------------+
| :mr:`2290` | Fix Eltex.MES5448.get_config script                                            |
+------------+--------------------------------------------------------------------------------+
| :mr:`2293` | Fix title and additional column to LinkDetailReport.                           |
+------------+--------------------------------------------------------------------------------+
| :mr:`2297` | Django 1.11.22                                                                 |
+------------+--------------------------------------------------------------------------------+
| :mr:`2309` | docs: Tools documentation                                                      |
+------------+--------------------------------------------------------------------------------+
| :mr:`2322` | black: Ignore deleted files                                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2323` | SA CLI/SNMP tests                                                              |
+------------+--------------------------------------------------------------------------------+
| :mr:`2327` | Add Address column to Latest Changes report.                                   |
+------------+--------------------------------------------------------------------------------+
| :mr:`2336` | Fix column name in ReportLinkDetail.                                           |
+------------+--------------------------------------------------------------------------------+
| :mr:`2349` | Update DLink.DxS_Smart.__init__.py add DES-1210-52 v4                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`2351` | Update Huawei.VRP.get_version.py add CE platform.                              |
+------------+--------------------------------------------------------------------------------+
| :mr:`2355` | Add DLink.DxS_Smart.get_capabilities for detecting of enabled LLDP protocol    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2365` | Add hw_version and bootpromversion to ManagedObject BI models.                 |
+------------+--------------------------------------------------------------------------------+
| :mr:`2376` | Add confdb support to Hikvision.DSKV8 profile.                                 |
+------------+--------------------------------------------------------------------------------+
| :mr:`2381` | Add confdb support to Beward.BD profile.                                       |
+------------+--------------------------------------------------------------------------------+
| :mr:`2395` | Add Eltex.WOP profile.                                                         |
+------------+--------------------------------------------------------------------------------+
| :mr:`2404` | docs: ConfDB query language                                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2405` | Fix doc typo                                                                   |
+------------+--------------------------------------------------------------------------------+
| :mr:`2412` | MR: Check `confdb` label                                                       |
+------------+--------------------------------------------------------------------------------+
| :mr:`2413` | Update NAG.SNR.get_arp.py                                                      |
+------------+--------------------------------------------------------------------------------+
| :mr:`2416` | ConfDB: Fix Query doc                                                          |
+------------+--------------------------------------------------------------------------------+
| :mr:`2421` | noc confdb syntax `path` parameter                                             |
+------------+--------------------------------------------------------------------------------+
| :mr:`2423` | docs: GA integration                                                           |
+------------+--------------------------------------------------------------------------------+
| :mr:`2429` | Add confdb normalizer to Dahua.DH profile.                                     |
+------------+--------------------------------------------------------------------------------+
| :mr:`2434` | check status http query                                                        |
+------------+--------------------------------------------------------------------------------+
| :mr:`2436` | CI: Disable test html report                                                   |
+------------+--------------------------------------------------------------------------------+
| :mr:`2440` | install-packages: -v flag                                                      |
+------------+--------------------------------------------------------------------------------+
| :mr:`2441` | Add connect() to some commands.                                                |
+------------+--------------------------------------------------------------------------------+
| :mr:`2442` | Extract collections to build docs                                              |
+------------+--------------------------------------------------------------------------------+
| :mr:`2449` | Update EdgeCore.ES profile                                                     |
+------------+--------------------------------------------------------------------------------+
| :mr:`2450` | Add ConfDB normalizer to Cisco.IOS profile.                                    |
+------------+--------------------------------------------------------------------------------+
| :mr:`2455` | config: web.max_upload_size configuration parameter                            |
+------------+--------------------------------------------------------------------------------+
| :mr:`2459` | login: register_last_login option                                              |
+------------+--------------------------------------------------------------------------------+
| :mr:`2460` | Update RU translation for Web services.                                        |
+------------+--------------------------------------------------------------------------------+
| :mr:`2461` | ./noc confdb: tokenizer and normalizer helpers                                 |
+------------+--------------------------------------------------------------------------------+
| :mr:`2472` | Add confdb to managedobject card backend.                                      |
+------------+--------------------------------------------------------------------------------+
| :mr:`2475` | Use django-media package                                                       |
+------------+--------------------------------------------------------------------------------+

Bugfixes
--------
+------------+-------------------------------------------------------------------------------------------+
| MR         | Title                                                                                     |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`1847` | Fix DLink.DVG.get_chassis_id script                                                       |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`1952` | Fix SKS.SKS.get_interfaces script                                                         |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2007` | Fix SKS.SKS.get_spanning_tree script                                                      |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2008` | Fix Alstec.24xx.get_interfaces script                                                     |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2009` | Fix detect Catalyst 4k platform                                                           |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2010` | Fix path for release Dockerfiles                                                          |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2017` | Fix Huawei.VRF.get_interfaces untagged from pvid.                                         |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2037` | Fix Generic.get_capabilities script when SNMP false.                                      |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2052` | Fix get_config scripts.                                                                   |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2056` | Fix TFortis.PSW get_interfaces.                                                           |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2058` | Fix bulk update IPAM address usage cache.                                                 |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2066` | ConfDB: NotMatch doesn't yield context if unresolved unbound variables left               |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2068` | Fix get_displayed_type method for clickhouse field.                                       |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2090` | Fix RouterOS parser                                                                       |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2097` | fix not ascii in description                                                              |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2104` | Fix fix-pip                                                                               |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2116` | fix_metric_qtech_vendors                                                                  |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2119` | fix get_version script for old H3C devices                                                |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2127` | Fix upstream_connected_graph_template.                                                    |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2128` | Fix Eltex.MES profile                                                                     |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2140` | Fix export inv.objectmodel to JSON                                                        |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2151` | Fix Huawei.MA5600T pattern more.                                                          |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2159` | Fix activator http_get params typo.                                                       |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2167` | Fix add user in docker release image                                                      |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2170` | Fix managed_object logger.                                                                |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2173` | Fix ipv4 address validator                                                                |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2175` | Fix inetrace speed attribute on ch dictionary                                             |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2177` | fixed H3C get_version for old devices like H3C S3100-8T-SI                                |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2183` | Fix datasource interfaceattributes dictionary.                                            |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2191` | Fix Cisco.IOSXR.convert_interface_name                                                    |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2199` | Fix caches                                                                                |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2203` | Fix telnet SB \.\. SE parsing                                                             |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2205` | Fix command_disable_pager for NAG.SNR.                                                    |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2208` | Fix reportmetrics field order.                                                            |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2211` | Fix trace when convert UUID field on extdocapplication.                                   |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2216` | Fix LRUcache missing on etl chain                                                         |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2230` | Fix typo in extdocapplication backend.                                                    |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2237` | Fix trace when check type for new column                                                  |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2247` | Profile: Compile syntax/operation error patterns as multiline                             |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2255` | Fix do_pending_operations in selectorcache.                                               |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2259` | noc/noc#1047 Delete unused code from prefix delete_recursive.                             |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2267` | Fix Huawei.MA5300.get_interfaces script                                                   |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2268` | Fix Tag search query.                                                                     |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2269` | Replace XML namespace parameter on profile Hikvision.DSKV8.                               |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2270` | Skip send_on_syntax_error when beef cli_error.                                            |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2274` | Fix prompt in Eltex.DSLAM profile                                                         |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2275` | Fix backport label check                                                                  |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2276` | Fix Qtech.QOS.get_version script                                                          |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2277` | Fix MikroTik.RouterOS.get_fqdn script                                                     |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2278` | Fix MikroTik.RouterOS.get_cdp_neighbors script                                            |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2279` | Add operation_error in Cisco.IOS profile                                                  |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2286` | Fix DCN.DCWL.get_interfaces profile for WL8200-TL1                                        |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2298` | Update Eltex.DSLAM profile                                                                |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2302` | Fix Beward.BD more than 1 value trace.                                                    |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2305` | Fix Caps model, Update caps when sync collections                                         |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2308` | Add yandex apikey configuration                                                           |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2317` | Fix software_image option on script command.                                              |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2326` | Fix DCN.DCWL.get_interface_status_ex for WL8200.                                          |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2340` | Fix regex for duplicates packets in DCN.DCWL.ping script.                                 |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2341` | Fix refresh cfgping datastream when timepattern change                                    |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2343` | Fix DialPlan and NetworkSegment links in Project Card                                     |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2347` | Update NAG.SNR.get_interfaces.py add QSFP+                                                |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2348` | Update Huawei.VRP.get_portchannel.py add dynamic                                          |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2350` | Update DLink.DxS_Smart.get_portchannel.py - fix "type" output                             |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2353` | simple report fixed                                                                       |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2356` | Update DLink.DxS_Smart.get_lldp_neighbors.py                                              |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2357` | reportmetrics fixed                                                                       |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2360` | Fix docker push command                                                                   |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2362` | Fix container column on ReportObjectDetail.                                               |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2364` | Return User.get_full_name() method, uses in ActiveAlarm backend.                          |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2366` | Fix ReportLinkDetail when empty tags.                                                     |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2367` | Add convert_interface_name to Iskratel.ESCOM.                                             |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2373` | fix_version_regex_eltex_mes                                                               |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2375` | fix_get_config_MXA24                                                                      |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2377` | Fix Alcatel.TIMOS profile. Trace when iface has empty MAC.                                |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2378` | Fix NSN.TIMOS.get_lldp_neighbors. Fix Multiline Remote PortsID and RemotePortDescription. |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2379` | fix_get_config_Eltex_RG                                                                   |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2380` | Add empty values to Reports choices fields.                                               |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2386` | Add `display omit` to Juniper `show configuration` command                                |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2387` | Fix Eltex.MES.get_version script on non stack devices                                     |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2388` | Fix deleted missing parameter on LRUCache.                                                |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2389` | Fix model cannot be resolved on managedobjectselector field.                              |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2390` | Add set_unusable_password method to User model.                                           |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2393` | noc/noc#1042                                                                              |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2396` | #1068 Fix SQL and QTags broken by django upgrade                                          |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2397` | #1064 Migrate Handlers                                                                    |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2398` | #1066 Refactored CachedForeignKeyField                                                    |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2399` | Fix Qtech.QSW8200.get_version regex.                                                      |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2402` | Fix DCN.DCWL.get_interface_status_ex trace if not bss return.                             |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2403` | Fix Alcatel.AOS.get_switchport untagged vlan list to int.                                 |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2407` | Fix AlarmEscalation wait_tt processing                                                    |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2414` | ConfDB: Fix syntax glitches                                                               |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2427` | Fix ./noc newapp                                                                          |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2432` | filter horizontal scroll fixed                                                            |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2443` | Move _archive_db attribute from archive bi extractor to method.                           |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2447` | Add configvalidation field on report_discovery result.                                    |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2448` | Fix Stream Audio config section on Hikvision.DSKV8.                                       |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2451` | ConfDB: Fix bound variables handling in NotMatch                                          |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2453` | users remove is_staff from model                                                          |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2457` | Fix User's preferred language                                                             |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2473` | Fix typo in Beward.BD normalizer.                                                         |
+------------+-------------------------------------------------------------------------------------------+
| :mr:`2474` | Fix Huawei.VRP.get_version on S5600-HI platform                                           |
+------------+-------------------------------------------------------------------------------------------+

Code Cleanup
------------
+------------+------------------------------------------------------------+
| MR         | Title                                                      |
+------------+------------------------------------------------------------+
| :mr:`1885` | Migrate KB to ExtModelApplication                          |
+------------+------------------------------------------------------------+
| :mr:`1977` | Model __str__ methods                                      |
+------------+------------------------------------------------------------+
| :mr:`2029` | Remove copy/paste mistake from Eltex.MES.get_config script |
+------------+------------------------------------------------------------+
| :mr:`2034` | noc-model-str-cm-facts2                                    |
+------------+------------------------------------------------------------+
| :mr:`2035` | noc-model-str-core-ip                                      |
+------------+------------------------------------------------------------+
| :mr:`2036` | noc-model-str-services-lib                                 |
+------------+------------------------------------------------------------+
| :mr:`2049` | Test model's __str__                                       |
+------------+------------------------------------------------------------+
| :mr:`2050` | py3 dict .iteritems(), .itervalues(), .iterkeys()          |
+------------+------------------------------------------------------------+
| :mr:`2051` | 2to3 except fix                                            |
+------------+------------------------------------------------------------+
| :mr:`2054` | 2to3 exec fix                                              |
+------------+------------------------------------------------------------+
| :mr:`2060` | Remove urllib usage in profiles                            |
+------------+------------------------------------------------------------+
| :mr:`2063` | test_base_parametrize. ver1                                |
+------------+------------------------------------------------------------+
| :mr:`2064` | Wrap urllib/urllib2 usage                                  |
+------------+------------------------------------------------------------+
| :mr:`2067` | wrap StringIO                                              |
+------------+------------------------------------------------------------+
| :mr:`2074` | 2to3 import fix                                            |
+------------+------------------------------------------------------------+
| :mr:`2075` | 2to3 has_key fix                                           |
+------------+------------------------------------------------------------+
| :mr:`2076` | 2to3 fix urlparse                                          |
+------------+------------------------------------------------------------+
| :mr:`2080` | wrap maketrans call                                        |
+------------+------------------------------------------------------------+
| :mr:`2081` | 2to3 print fix                                             |
+------------+------------------------------------------------------------+
| :mr:`2082` | 2to3 fix `map` and `filter`                                |
+------------+------------------------------------------------------------+
| :mr:`2083` | 2to3 imports fix                                           |
+------------+------------------------------------------------------------+
| :mr:`2085` | 2to3 itertools and itertools_import fixes                  |
+------------+------------------------------------------------------------+
| :mr:`2086` | 2to3 long fix                                              |
+------------+------------------------------------------------------------+
| :mr:`2089` | 2to3 types fix                                             |
+------------+------------------------------------------------------------+
| :mr:`2094` | test_ecma48                                                |
+------------+------------------------------------------------------------+
| :mr:`2095` | test_ber                                                   |
+------------+------------------------------------------------------------+
| :mr:`2101` | Remove south usage from BaseMigration class                |
+------------+------------------------------------------------------------+
| :mr:`2106` | Migration Runner, Bye-bye South                            |
+------------+------------------------------------------------------------+
| :mr:`2107` | Cleanup models' __init__.py                                |
+------------+------------------------------------------------------------+
| :mr:`2120` | fix_DeprecationWarning_main_0049_update_tags               |
+------------+------------------------------------------------------------+
| :mr:`2121` | fix_test_ip                                                |
+------------+------------------------------------------------------------+
| :mr:`2123` | test_crypto                                                |
+------------+------------------------------------------------------------+
| :mr:`2124` | test_mac                                                   |
+------------+------------------------------------------------------------+
| :mr:`2133` | remove_total_seconds                                       |
+------------+------------------------------------------------------------+
| :mr:`2135` | test_matcher                                               |
+------------+------------------------------------------------------------+
| :mr:`2136` | test_validators                                            |
+------------+------------------------------------------------------------+
| :mr:`2221` | docs format mr tables                                      |
+------------+------------------------------------------------------------+
| :mr:`2236` | Fix docs path                                              |
+------------+------------------------------------------------------------+
| :mr:`2242` | Fix mongoengine imports                                    |
+------------+------------------------------------------------------------+
| :mr:`2243` | Fix mongoengine imports                                    |
+------------+------------------------------------------------------------+
| :mr:`2251` | Clean Huawei.MA5600T profile                               |
+------------+------------------------------------------------------------+
| :mr:`2263` | 2to3: zip fix                                              |
+------------+------------------------------------------------------------+
| :mr:`2264` | Remove unused cm templates                                 |
+------------+------------------------------------------------------------+
| :mr:`2265` | 2to3: `next` fix                                           |
+------------+------------------------------------------------------------+
| :mr:`2266` | Fix ObjectId import                                        |
+------------+------------------------------------------------------------+
| :mr:`2271` | 2to3: `dict` fix                                           |
+------------+------------------------------------------------------------+
| :mr:`2283` | 2to3: `xrange` fix                                         |
+------------+------------------------------------------------------------+
| :mr:`2291` | black: aaa, bi, cm                                         |
+------------+------------------------------------------------------------+
| :mr:`2306` | black: crm, dev, dns, fixes, fm                            |
+------------+------------------------------------------------------------+
| :mr:`2307` | black: gis, inv, ip, kb                                    |
+------------+------------------------------------------------------------+
| :mr:`2310` | fix_import_lib_nosql_part1                                 |
+------------+------------------------------------------------------------+
| :mr:`2311` | fix_import_lib_nosql_part2                                 |
+------------+------------------------------------------------------------+
| :mr:`2314` | black: migrations                                          |
+------------+------------------------------------------------------------+
| :mr:`2315` | fix_import_lib_nosql_part3                                 |
+------------+------------------------------------------------------------+
| :mr:`2316` | fix_import_lib_nosql_part4                                 |
+------------+------------------------------------------------------------+
| :mr:`2318` | black: sa                                                  |
+------------+------------------------------------------------------------+
| :mr:`2319` | black: lib                                                 |
+------------+------------------------------------------------------------+
| :mr:`2320` | black: core                                                |
+------------+------------------------------------------------------------+
| :mr:`2321` | black: Rest of stuff                                       |
+------------+------------------------------------------------------------+
| :mr:`2330` | Bump version                                               |
+------------+------------------------------------------------------------+
| :mr:`2354` | Add mongo connect to commands.                             |
+------------+------------------------------------------------------------+
| :mr:`2358` | Speedup docker release images build with targeted builds   |
+------------+------------------------------------------------------------+
| :mr:`2406` | Drop unused fields                                         |
+------------+------------------------------------------------------------+
| :mr:`2411` | ConfDB syntax refactoring                                  |
+------------+------------------------------------------------------------+
| :mr:`2422` | Move profiles to profile.py                                |
+------------+------------------------------------------------------------+
| :mr:`2424` | Fix get_version Infinet.Wanflex                            |
+------------+------------------------------------------------------------+
| :mr:`2428` | Clean up noc.lib.nosql imports                             |
+------------+------------------------------------------------------------+
| :mr:`2439` | Fix documentation glitches                                 |
+------------+------------------------------------------------------------+
| :mr:`2452` | Update Dynamic Dashboards.                                 |
+------------+------------------------------------------------------------+