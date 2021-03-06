.. _release-0.4:

=================
0.4 (11-APR-2010)
=================

Migration
---------
* Upgrade mercurial to version 1.3 or later before fetching updates

General
-------
* User interface is cleaned up
* contrib/ directory contains third-party software: Django 1.1.1, South 0.6.2, flup 1.0.2, protobuf 2.2.0a, python-creole 0.2.4, pyasn1 0.0.9a, pysnmp 4.1.12a, Pygments 1.2.2, docutils 0.6, Jinja2 2.2.1, Sphinx 0.6.4, Coverage 3.3.1
* Unittest coverage reports for "manage.py test"

Main
----
* pyRules

Address Space Management
------------------------
* Display addressess within /32 blocks properly

Service Activation
------------------
* Juniper.JUNOS profile supports "with self.configure():" construction in scripts
* New interface parameters: IPv4Prefix
* New interfaces: ISyncPrefixLists, IReduceScript
* New scripts: Juniper.JUNOS.sync_prefix_lists
* Profile Alcatel.AOS renamed to Alcatel.OS62xx
* New Alcatel.AOS profile
* Profile VoiceFinder.AddPack renamed to AddPac.APOS
* Built-in TFTP server

DNS Management
--------------
* Sort reverse zones' PTR records as numbers

Peering Management
------------------
* PeeringPoint.enable_prefix_list_provisioning periodic task
* Prefix-List provisioning
* Peer.local_backup_ip and .remote_backup_ip fields
* PeerGroup.local_pref, .import_med and .export_med fields
* Peer.import_med and .export_med fields

Virtual Circuit Management
--------------------------
* VC Bind Filters

