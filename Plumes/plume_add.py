#!/usr/bin/env python 
import sys
import os
import math

from plume_buffer import addPlumes

def getArgs():
    try:
        filename = sys.argv[1]
        prefix = filename.split('.')[0] # file prefix only 
        return prefix
    except:
        print sys.argv[0] + " usage: <output filename>"
        sys.exit(1)

###############################################
if __name__ == '__main__':

    prefix = getArgs()
    addPlumes("%s.img" % prefix)
