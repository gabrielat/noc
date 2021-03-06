.. _release-15.05:

=========
NOC 15.05
=========


Requirements
------------

* NOC no longer depends on PostGIS
* MongoDB 2.4 or later required (MongoDB 3.0 with `WiredTiger <http://www.wiredtiger.com/>`_ storage engine recommended)

Infrastructure
--------------

* Customer portal cp.nocproject.org has been intruduced.
* Support module allows to collect and share tracebacks and reports about upgrade problems
* NOC can be extended via custom or third-party solutions
* One-command NOC node deployment
* NOC nodes can be updated from master node

UI
--

* General UI cleanup
* Vector glyphs are used instead of icons
* Retina-friendly
* ExtJS 5.1
* Pagerless Model Applications
* Group editing
* Tree Filter

Service Activation
------------------

* Monitor application
* Improved stability and logging
* Greatly improved performance
* Built-in ssh client supports ECDSA, improved ssh servers compatibility
* Lots of new profiles and scripts
* Great amount of bugfixes
* AuthProfiles to store shared credentials
* Actions as generalized command snippets
* ./noc cli-commands for batch command executing

Configuration Management
------------------------

* Config validation framework built around `CLIPS <http://clipsrules.sourceforge.net/>`_ expert system
* Cisco.IOS, Cisco.IOSXR, Juniper.JUNOS, DLink.DxS and Mikrotik.RouterOS parser
* FM alarms are generated on policy violations

Fault Management
----------------

* Event- and alarmclasses can be created via UI
* Lots of new classes and rules
* noc-classifier speedup
* Experimental rule matcher accelerator

Inventory
---------

* Map preview
* Rack layout
* Lots of object models
* Cable conduits
* Connection rules and generic get_asset scripts simplification
* ip discovery can be set on per-prefix basis
* Prevent SA system overloading by discovery process
* Sophisticated job scheduling

Performance Management
----------------------

* Distributed PM infrastructure inspired by `Graphite <http://graphite.wikidot.com/>`_
* Compact pluggable data storage (MongoDB or RocksDB).
  See `KVS comparison <https://www.evernote.com/l/ADnckwK0Be5E97cZpD2V2BOwQFyJG5sJHjI>`_ for details
* Graphite-compatible API for data fetching and manipulation
* Automatic probe configuration on database changes
* Integrated `Grafana <http://grafana.org/>`_ dashboard

DNS
---

* Simple HTTP-based synchronisation scheme
* Various zone-generation fixes
