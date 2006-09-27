#!/usr/bin/python

import sys

def parseMatrix(matrix_file):
    matrix = {
              'threat1': {'habitat1': 4, 'habitat2':2} ,
              'threat2': {'habitat1': 3, 'habitat2':1} 
             }
    # TODO read csv
    # TODO put into dictionary
    #      (if something goes wrong, throw exception)
    return matrix

def processThreatHabitatCombo(threat,habitat,weight):
    # TODO make sure both layers exist
    # TODO mapcalc em together
    valid = True
    output = threat + "_" + habitat
    return {'valid': valid, 'output': output }

def processAllCombos(combos):
    output_map = "model_output"
    mapcalc  = " r.mapcalc %s = \"" % output_map
    mapcalc += ' + '.join(combos)
    mapcalc += "\""
    # TODO  Check if everything went OK
    print mapcalc
    valid = True
    return {'valid': valid, 'output': output_map} 
        

if __name__ == "__main__":
    try:
        matrix_file = sys.argv[1]
    except:
        # TODO check for valid file
        #sys.exit(1)
        pass

    matrix = parseMatrix(matrix_file)

    threat_combos = []

    for threat in matrix.keys():
        for habitat in matrix[threat].keys():
            response = processThreatHabitatCombo(threat,habitat,matrix[threat][habitat])
            if response['valid']:
                threat_combos.append(response['output'])
                print response['output']    
                print " Weighting = %s " % matrix[threat][habitat]
            else:
                print "%s / %s  combination failed" % (threat, habitat)

    response = processAllCombos(threat_combos)
    if response['valid']:
        print "Your model result is ... '%s'" % response['output']

