.. _release-0.1RC2:

====================
0.1RC2 (29-JAN-2009)
====================

General
-------
* site_settings.py replaced with etc/noc.ini configuration file
* daemons reload config on SIGHUP
   
Main
----
* main.backup periodic back ups repo too
* New reports: main.system report, main.backups report
* New periodicts: main.cleanup_sessions

Peering Management
------------------
* Maintainer object

Service Activation
------------------
* New service activation framework with scripting support
* script interfaces
* generic scripts
* gzip message compression between SAE and activators
* Activator tries to reconnect to SAE on connection lost
* Activator digest authentication
* manage.py debug-profile replaced with manage.py debug-script
   
Configuration Management
------------------------
* Configuration management uses service activation now
* New reports: cm.stale_configs

Fault Management
----------------
* Initial Fault Management implementation
* noc-classifier daemon
* SNMP Trap and Syslog collector
* MIB compilation and uploading
