.. _release-0.2.7:

===================
0.2.7 (05-AUG-2009)
===================

Main
----
* Flexible notification mechanism with Time Patterns and Notification Groups and noc-notifier daemon
* User Profiles
* noc-launcher can set up daemons user and group ids
* DeprecationWarnings on python 2.6 are removed
* Record preview in Reference Books
* Old backup removal
* All daemons silently exit on SIGINT signal
* All daemons accept --version key
* manage.py "build-manifest" command

Service Activation
------------------
* Optional SSL encryption of SAE-Activator stream
* DLink.DGS3xxx profile now supports DGS3100

Configuration Management
------------------------
* Do not raise exception on yet-not-read config previewing

Fault Management
----------------
* Ping only active managed objects
* Managed Object lookup is case insensitive now
* Case-insensitive search over Managed Objects in event filter
* New event classes: "Config Synced", "Bad DNS Query"
* New classification rules for Cisco.IOS
* Repeat protection for "Invalid Event Source" event

Peering Management
------------------
* Configurable RPSL's pref- symantics (localpref or 65535-localpref)

Knowledge Base
--------------
* "reserved" attribute of "allocation" tag in "rack" macro
