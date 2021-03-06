.. _release-0.3:

=================
0.3 (02-SEP-2009)
=================

Main
----
* System Notifications
* etc/noc.conf: new configuration options: month_day_format and year_month_format
* Basic GnuPG support

Address Space Management
------------------------
* Display a list of block maintainers in block info
* VRF and VRF Groups description fields
* Show breadcrumbs in IP Address Assignment form

Service Activation
------------------
* New profiles: Zyxel.ZyNOSv2, HP.iLO2, Cisco.NXOS, Cisco.AireOS, Raisecom.ROS
* Cisco.IOS.get_version uses SNMP when available
* Cisco.IOS.get_mac_address_table: improved compatibility with IOS GS (Catalyst 4500 series)
* SAE creates missed task schedules
* SAE generates events of periodic task completion
* "Run Now" link in Task Schedules form
* New interfaces: IGetDHCPBinding, IGetLocalUsers, IHasLocalUser
* New scripts: Cisco.IOS.get_dhcp_binding, Cisco.IOS.get_local_users, Force10.FTOS.get_local_users, Generic.has_local_user, Cisco.NXOS.get_local_users
* New interface parameter availeble: DateTimeParameter
* Memory and thread leaking in noc-activator fixed

Fault Management
----------------
* New event classes, classification and correlation rules rules for Performance Management, Periodic tasks and Cisco.IOS
* Activator places "collector" signature into the events
* Event preview form shows descriptions from MIB
* New MIBs: AIRESPACE-REF-MIB, AIRESPACE-WIRELESS-MIB, CISCO-LWAPP-AAA-MIB, CISCO-LWAPP-TC-MIB, CISCO-LWAPP-WLAN-MIB

DNS Management
--------------
* Domain expiration checking (DNSZone.paid_till field and dns.check_domain_expiration periodic task)
* Registrar database synchronization (dns.update_domain_expiration periodic task)
* Import zones from text file
* Nested zones handling improved
* Missed A records for zone nameservers are auto-created

Performance Management
----------------------
* New performance management framework
* Basic set of probes: tcp, http, smtp, ssh, snmp, snmp-interface, popen, process
* manage.py ts-list, ts-rm, ts-export commands

Knowledge Base
--------------
* Show article categories at the bottom of article
* "Categories" page
* "label" attribute of "rackset" tag in "rack" macro
* Sortable CSV tables
