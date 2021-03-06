.. _release-0.6.4:

===================
0.6.4 (03-MAY-2011)
===================

Migration
=========
Rename max_pull_config parameter in etc/noc-activator.conf to
max_scripts

Common
======

noc-schedule daemon
-------------------
Periodic task handling moved from SAE to a new noc-schedule daemon,
improving overall SAE stability. Custom pyRules can be launched as
common periodic tasks, allowing deep NOC customization.

contrib/
--------
contrib/ directory contains updated versions of following packages:

* Django 1.3
* Sphinx 1.0.7

sendmail method
---------------
noc-notifier supports new "sendmail" method, allowing to spool new messages
directly to local mail-agent queue. This method is compatible with
nullmailer. It also can be used to spool messages to arbitrary scripts.

PEP8 compliance
---------------
Large amont of python modules are reformatted according to PEP8 proposal.

Clean up forgotten map-reduce tasks
-----------------------------------
main.cleanup periodic task also removes hanging Map/Reduce tasks data.

Prefix Tables
-------------
Prefix Tables are named lists of IPv4/IPv6 prefixes, which can be used
for configuration purposes in many places. 0.6.4 release allows to
use Prefix Tables in Managed Objects Selectors

Service Activation
==================

SA Sharding
-----------
Service Activation subsystem can be split into several independing shards,
each having dedicated activators and SAE daemons. Sharding opens new ways
for horizontal scaling of large installations. In addition, shard can be
put offline, disabling only part of SA subsystem for maintainance.

WRR load balancing
------------------
Activator reports its capabilities (including script session limits)
to SAE on connect. SAE uses weighted round-robin (WRR) balancing scheme
to proportionally distribute the load between activators in the pool.

Command Snippets
----------------
Command Snippets are canned parametrized templates for frequenly-used
operations, which can be run multiple times on large amount of equipment.

Script output templating
------------------------
Scripts launched from Managed Object's script form now utilize neat
HTML templates with additional hot actions links.

Input encodings
---------------
Treat Managed Object's _encoding_ attribute as input encoding specification

Per-object concurrent scripts limit
-----------------------------------
Managed Object's _max_scripts_ attribute is used as per-object concurrent
scripts limit

max_pull_config renamed
-----------------------
noc-activator's max_pull_config parameter is renamed to less obsfucated
max_scripts

Larger remote_path
------------------
ManagementObject.remote_path can be up to 256 characters

API improvements
----------------

* Profile.shutdown_session() - profiles can use scriptable session shutdowns, similar to start_session()
* ManagedObject.scripts - all scripts can be accessed directly via .scripts property

New profiles
------------

* ZTE.ZXR10

New interfaces
--------------

* IGetHTTPGet
* IGetLicense
* IGetSNMPGet
* IGetSNMPGetNext

New scripts
-----------
* EdgeCore.ES.get_switchport
* Force10.FTOS.ping
* Generic.get_http_get
* Generic.get_snmp_get
* Generic.get_snmp_getnext
* f5.BIGIP.get_arp
* f5.BIGIP.get_licence
* f5.BIGIP.ping

Compatibility
-------------
Better compatibility for:

* D-Link DGS-3120 Series
* Cisco Catalyst 2950

get_version optional attributes
-------------------------------
get_version can return additional named attributes

Non-blocking HTTP client
------------------------
Non-blocking http client introduced for accurate timeout handling

ssh: keyboard-interactive method
--------------------------------
Built-in ssh daemon can authenticate using keyboard-interactive method

f5.BIGIP uses bash
------------------
f5 devices must be configured to use advanced shell (bash) for noc user.

Event filters are refreshed on object's address changed
-------------------------------------------------------
Event filters are reloaded immediately when managed object's addresses
are changed, reducing amount of Invalid event filter events

Bugfixes
--------

* Prevent recursive selectors creation
* Unicode logging issues
* Error handling in HTTP
* Better handling of Telnet/SSH connection timeout

Configuration Management
========================

"Get now" retrieves config immediately
--------------------------------------
"Get now" admin action immediately refetches selected configs instead
of rescheduling next pull

Filter by "Administrative domain"
---------------------------------
"Administrative domain" filter is added to config list pane

DNS
===
Flexible zone changes notifications
-----------------------------------
Multi-level DNS Zone changes notifications are introduced. Notification Group
used to report zone changes calculated in following order: First, try to use
DNS Zone's group, if set. For empty DNS Zone's group try to use one from
DNS Zone profile. Finally, if no group is set for profile, use system's
notification group

.ip6.arpa zones treated as IPv6 reverse
---------------------------------------
.ip6.arpa zones are treated as usual IPv6 reverse zones
