#!/usr/bin/python
"""
  Threat Matrix Combination Script

  For each threat/habit combo, combine them into a single
  raster. While the martix file is needed to define the
  threats and habitats, the weighting values are not 
  applied until you run the actual model (threat_model.py)

  The matrix file will have the following format:

    ,habitat1,habitat2
    threat1,4,2
    threat2,3,1

  Author: Matthew Perry
  Date: 09/27/2006
"""

import sys
import os

def parseMatrix(matrix_file):
    try:
        fh = open(matrix_file, 'r')
        lines = fh.readlines()
    except:
        print "can't read matrix file"
        sys.exit(1)

    habitats = lines[0].replace('\n','').split(',')[1:]
    threats = []
    for i in (range(1,len(lines))):
        threat = lines[i].replace('\n','').split(',')[0]
        if threat != '' and threat is not None:
            threats.append(lines[i].replace('\n','').split(',')[0])

    return threats, habitats

def processThreatHabitatCombo(threat,habitat):
    # TODO make sure both layers exist
    # TODO mapcalc em together
    output = "combo_" + threat + "_" + habitat
    mapcalc = "r.mapcalc %s = '%s * %s'" % (output, threat, habitat) 
    print mapcalc
    response = os.popen(mapcalc).read().rstrip()
    print response
    print 
    valid = True
    return {'valid': valid, 'output': output }


if __name__ == "__main__":
    try:
        matrix_file = sys.argv[1]
    except:
        print " usage: generate_combos.py matrix_file.txt"
        sys.exit(1)

    threats,habitats = parseMatrix(matrix_file)


    for threat in threats:
        for habitat in habitats:
            response = processThreatHabitatCombo(threat,habitat)
            if response['valid'] is not True:
                print "%s / %s  combination failed" % (threat, habitat)

