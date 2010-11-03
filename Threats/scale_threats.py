#!/usr/bin/python
"""
 Scale threats layers from 0 to 1 (continous).
 Assumes all threat layers are prefixed "prethreat_"

"""

import os
import sys

threatlist = os.popen('g.mlist type=rast pattern=prethreat*').readlines()

for threat in threatlist:
    threat = threat.replace('\n','')
    print threat
    # Get the min/max
    range = {}
    for line in os.popen('r.info -r ' + threat).readlines():
        linesplit = line.replace('\n','').split('=')
        range[linesplit[0].strip()] = float(linesplit[1].strip())
    print "min = %s ... max = %s" % (range['min'],range['max'])   
    mapcalc = "r.mapcalc %s = 'if( isnull(%s), 0 , float(%s) / %s)' " % \
              (threat.replace('prethreat','threat'), threat, threat, range['max'])
    print os.popen(mapcalc).read()
    print "-----------------------"
