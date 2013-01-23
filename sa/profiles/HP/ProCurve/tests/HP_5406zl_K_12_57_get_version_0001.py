# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## HP.ProCurve.get_version test
## Auto-generated by ./noc debug-script at 21.01.2013 18:15:10
##----------------------------------------------------------------------
## Copyright (C) 2007-2013 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class HP_ProCurve_get_version_Test(ScriptTestCase):
    script = "HP.ProCurve.get_version"
    vendor = "HP"
    platform = "5406zl"
    version = "K.12.57"
    input = {}
    result = {'platform': '5406zl', 'vendor': 'HP', 'version': 'K.12.57'}
    motd = ''
    cli = {
'terminal length 1000':  'terminal length ', 
'walkMIB sysDescr':  'walkMIB sysDescrsysDescr.0 = ProCurve J8697A Switch 5406zl, revision K.12.57, ROM K.12.12 (/sw/c\node/build/btm(t2g))\n', 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
