#!/usr/bin/env python 
import sys

from plume_buffer import addPlumes

def getArgs():
    try:
        filename = sys.argv[1]
        prefix = filename.split('.')[0] # prefix only 
        attribute = sys.argv[2]
        return prefix, attribute
    except:
        print sys.argv[0] + " usage: <output filename> <attribute>"
        sys.exit(1)

###############################################
if __name__ == '__main__':

    prefix, attribute = getArgs()
    addPlumes("%s.img" % prefix, attribute)
