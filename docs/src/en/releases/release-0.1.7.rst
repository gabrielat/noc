.. _release-0.1.7:

===================
0.1.7 (16-MAR-2009)
===================

Migration
---------
* Set up 'dig' path in [path]/dig option in etc/noc.conf
* Migration process is simplified. Just after update perform::

    su - noc
    cd /opt/noc
    ./scripts/post-install
  
Main
----
* [path]/dig option in etc/noc.conf
* Autodetection of paths in `etc/*.conf` files in post-install script
* Integrated online documentation (Administrator's and User's Guides)

Service Activation
------------------
* f5 BIG-IP basic support
* Improved handling of pagers
* Juniper.JUNOS.get_version SRX platform support
* Serialization error when non-empty ManagedObject.port is fixed
* Better handling of XML-RPC failures in web interface

Fault Management
----------------
* "Clone Rule" button in Event Classification Rule form
