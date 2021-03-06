.. _release-0.3.2:

===================
0.3.2 (12-DEC-2009)
===================

Service Activation
------------------
* Embedded FTP server
* New profiles: Raritan.DominionSX
* New scripts: Generic.configure, HP.GbE2.get_vlans, HP.GbE2.add_vlan, HP.GbE2.remove_vlan

Fault Management
----------------
* New MIBs: FORCE10-TC, FORCE10-SMI, F10-CHASSIS

Configuration Management
------------------------
* "Get Now" link in config index
* Mutli-file configurations

Address Space Management
------------------------
* IPv4 Block to VC binding
* Link to change block access directly from block view

Peering Management
------------------
* Whois Cache
* peer.update_whois_cache periodic task
* Interactive prefix-list builder
* AS RPSL builder reworked
* Organisation objects
* Peer.status, Peer.rpsl_remark, AS.as_name, AS.admin-c, AS.tech-c, AS.maintainters, AS.route-maintainers fields
* RIPE database auto-update

Performance Management
----------------------
* jQuery extension for time series preview
* Time Series preview

Virtual Circuit Management
--------------------------
* VC Provisioning for HP.GbE2
* Display bound IPv4 blocks in VC list
