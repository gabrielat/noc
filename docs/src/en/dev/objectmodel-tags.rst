.. _dev-objectmodel-tags:

================
ObjectModel Tags
================

.. contents:: On this page
    :local:
    :backlinks: none
    :depth: 1
    :class: singlecol

*ObjectModel* may contain additional tags, containing additional
information about component's capabilities

Common Tags
-----------
* `chassis` - chassis (equipment body)
* `lc` - linecard, optional replaceable module (except for fans and PSU)
* `xcvr` - transceiver
* `psu` - power supply unit
* `sup` - supervisor or control module (control plane)
* `fabric` - commutation fabric (data plane)
* `fan` - fan
* `soft` - software component
* `port` - contains ports acceptable for client connection either directly or via transceiver
* `dsp` - digital signal processor for voice/video processing

Tags may be combined together:

* `chassis`, `sup`, `psu`, `fabric`, `ports` - fanless access switch
* `chassis`, `sup`, `psu`, `fabric`, `ports`, `fan` - access switch with active cooling
* `lc`, `port` - linecard with ports
* `sup`, `fabric`, `lc`, `port` - supervisor with integrated fabric and ports
