#!/usr/bin/python
"""
  Threat Matrix Model

  For each threat/habit combo (already created using 
  generate_combos.py), add them according to
  weighting defined in a matrix file. The final output
  is the sum of all weighted combinations.

  The matrix file will have the following format:

    ,habitat1,habitat2
    threat1,4,2
    threat2,3,1

  Author: Matthew Perry
  Date: 09/26/2006
"""

import sys
import os
import time

def parseMatrix(matrix_file):
    try:
        fh = open(matrix_file, 'r')
        lines = fh.readlines()
    except:
        print "can't read matrix file"
        sys.exit(1)

    habitats = lines[0].replace('\n','').replace('\r','').split(',')[1:]
    matrix = {}
    for h in habitats:
        matrix[h] = {}

    for i in (range(1,len(lines))):
        line = lines[i].replace('\n','').replace('\r','').split(',')
        threat = line[0]
        values = line[1:]
        #print "\n%s\n" % threat + "-" * 20
        weights = {}
        for j in (range(0,len(habitats))):
            #print "%s = %s" % (habitats[j], values[j])
            matrix[habitats[j]][threat] = float(values[j])
            #weights[habitats[j]] = float(values[j])

    print
#    print matrix
    print
    return matrix

def processAllCombos(matrix,output_map):
    habitat_combos = []
    for habitat in matrix.keys():
        weighted_terms = []
        for threat in matrix[habitat].keys():
            #TODO check that combo layer exists
            input = "combo_" + threat + "_" + habitat
            weight = matrix[habitat][threat]
            weighted_terms.append("(%s * %s)" % (weight, input) )

        # weighted terms now contains a list of habitat<->threat pairs for a specific _habitat_
        habitat_combo_name = '%s_combo' % habitat
        habitat_combos.append(habitat_combo_name)
        habitat_mapcalc = " r.mapcalc %s = '%s'" % (habitat_combo_name, ' + '.join(weighted_terms))
        #print "\n\n CALCULATING FOR %s" % habitat + "-" * 40 + "\n%s" % habitat_mapcalc 

        response = os.popen(habitat_mapcalc)
        print response

    # threading causes contention issues, so wait for all threads to sync in cheapass way
    duration = 180
    time.sleep(duration)
    print "Waiting for %i seconds for threads to finish..." % duration

    mapcalc = " r.mapcalc %s = '%s'" % (output_map, ' + '.join(habitat_combos))
    print mapcalc
    #sys.exit()
    response = os.popen(mapcalc).read().rstrip()
    print response

    # TODO check validity of output map
    valid = True
    return {'valid': valid, 'output': output_map} 

if __name__ == "__main__":
    try:
        matrix_file = sys.argv[1]
        output_map = sys.argv[2]
    except:
        print "usage: threat_model.py matrix_file.txt output_grass_map"
        sys.exit(1)

    matrix = parseMatrix(matrix_file)
    response = processAllCombos(matrix,output_map)
    if response['valid']:
        print "Your model result is ... '%s'" % response['output']
