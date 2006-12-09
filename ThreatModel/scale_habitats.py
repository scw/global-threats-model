#!/usr/bin/python
"""
Take a raster habitat map and make a binary (presence or absence)
habitat map.

Assumes all habitat grass rasters are named "prehabitat_*"
"""

import os
import sys

habitatlist = os.popen('g.mlist type=rast pattern=prehabitat*').readlines()

for habitat in habitatlist:
    habitat = habitat.replace('\n','')
    print habitat
    mapcalc = "r.mapcalc %s = 'if(isnull(%s), 0, if(%s == 0, 0, int(1)))' " % \
              (habitat.replace('prehabitat','habitat'), habitat, habitat)
    print os.popen(mapcalc).read()
    print "=========================="
