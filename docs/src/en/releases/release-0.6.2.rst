.. _release-0.6.2:

===================
0.6.2 (16-FEB-2011)
===================

General
=======

New commiters
-------------

* Alexey Shirokih - Alcatel.TIMOS profile
* Dmitry Roshin - HP.ProCurve9xxx profile

noc-launcher
------------
noc-laucher can start multiple instances of single daemon. From now on you can
start several instances of noc-activator

Customizable favico.ico
-----------------------

Custom favico can be set via etc/noc.conf:[customization]/favicon_url parameter.
There are 4 icons of different colors placed into the repo.

Service Activation
==================

Activator Pools
---------------
From 0.6.2 release SAE permits to register sevaral activators with same name at once.
Such activators are groupped to the activator pools and SAE perfoms round-robin load
balance between the members of pool, increasing overall reponsibility, performance and redundancy.

API Improvements
----------------
* Timeout for reduce task detected automatically, if not set explicitly

UI improvements
---------------
* Compact table layout in "Managed Objects"

Address Space Management
========================
* 'Show free prefixes' link
* Recursive deleting of block
* Prefix rebasing
