#!/usr/bin/python
"""
  Threat Matrix Combination Model

  For each threat/habit combo, combine them according to
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

def parseMatrix(matrix_file):
    try:
        fh = open(matrix_file, 'r')
        lines = fh.readlines()
    except:
        print "can't read matrix file"
        sys.exit(1)

    habitats = lines[0].replace('\n','').split(',')[1:]
    matrix = {}
    for i in (range(1,len(lines))):
        line = lines[i].replace('\n','').split(',')
        threat = line[0]
        weights = {}
        for j in (range(1,len(habitats))):
            weights[habitats[j]] = float(line[j])

        matrix[threat] = weights

    print
    print matrix
    print
    return matrix

def processAllCombos(matrix,output_map):
    weighted_terms = []
    for threat in matrix.keys():
        for habitat in matrix[threat].keys():
            #TODO check that combo layer exists
            input = "combo_" + threat + "_" + habitat
            weight = matrix[threat][habitat]
            weighted_terms.append("(%s * %s)" % (weight, input) )
    mapcalc  = " r.mapcalc %s = \"" % output_map
    mapcalc += ' + '.join(weighted_terms)
    mapcalc += "\""
    print mapcalc

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



