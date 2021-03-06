.. _release-0.1.1:

===================
0.1.1 (11-FEB-2009)
===================

General
-------
* Various bugfixes
* Documentation improvements

Virtual Circuit Management
--------------------------
* New module: vc. Database of 802.1Q VLANs, 802.1ad Q-in-Q VLAN stacks, FR DLCI, ATM VPI/VCI, MPLS labels, X.25 logical group/channels

Address Space Management
------------------------
* IP addresses export/import to/from CSV file
* IP addresses can be imported directly via zone transfer

Service Activation
------------------
* New script interface - IGetDot11Associations
* Cisco.IOS.get_dot11_associations, ZTE.ZXDSL531.get_dot11_associations scripts
* Not registered activator no longer breaks config pulling process

Fault Management
----------------
* Activator can check managed objects availability via fping and raise FM events
* All unhandled exceptions in daemons passed as events to FM
