#!/usr/bin/python
"""
 Determines presence and absence of threat layers be reclassifying
     them into 0 or 1 and then sums the final products into a threat
     count sum
 Assumes all threat layers are prefixed "threat_"

"""

import os
import sys

threatlist = os.popen('g.mlist type=rast pattern=threat_*').readlines()

for threat in threatlist:
    threat = threat.replace('\n','')
    print threat
    #mapcalc = "r.mapcalc %s = 'if(%s > 0, 1 , 0)' " % \
    #          (threat.replace('threat','binary_threat'), threat)
    #print os.popen(mapcalc).read()
    print "-----------------------"

presabslist = os.popen('g.mlist type=rast pattern=binary_threat_*').readlines()

print presabslist
for presabs in presabslist:
    #presabslist.join(" + ")
    #mapcalc = "r.mapcalc = presabslist"
    #presabs = presabs.replace('\n' + '')
    #print "adding threat presences"
    #mapcalc = threat_pres_sum = presabs
    #print "done"
