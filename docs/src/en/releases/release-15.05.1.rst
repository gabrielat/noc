.. _release-15.05.1:

===========
NOC 15.05.1
===========



Release highlights
------------------

* Profiling and optimisation of FM, improved performance and stability
* Fixed inventory objects' attribute setting
* Easier migration from contrib/-based releases (0.7(2) and earlier)

Main
----

* JSON Import application

Inventory
---------

* Fixed: *Cannot update 'data.xxx' and 'data.xxx.yyy' at the same time*
* Lots of transceiver models
* Unimited amount of part_no and order_part_no entries in ObjectModel
* asset_discovery detects trash in vendor_id/part_no

SA
--

* New profiles: Supertel.K2X, HP.1910
* SAE: Batched events write
* CLI_TIMEOUT setting processed by telnet sessions correctly
* New scripts and fixes
* noc-activator's ping no longer generates lots of events on startup

FM
--

* More reliable reboot detection in uptime_discovery
* Reboots report
* Limit amount of MRT jobs started by noc-correlator
* Improved page refresh policy in Events and Alarms applications
* noc-classifier and noc-correlator performance tuning
* check_link alarm job can accept full interface status dump

CM
--

* Config validation performed in single thread
* New validators:

  * Hostname MUST NOT be empty
  * Interface MUST HAVE proxy arp disabled
  * Interface MUST HAVE ip redirects disabled
