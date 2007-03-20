#!/usr/bin/env python 
import sys
import os
import math

from plume_buffer import getCatList, cleanHouse

def getArgs():
      try:
          vectorpours = sys.argv[1]
          attrib = sys.argv[2]
          return vectorpours,attrib
      except:
          print sys.argv[0] + " usage: <vector name> <attribute>"
          sys.exit(1)

if __name__ == '__main__':
    pours, attrib = getArgs()

    catlist = getCatList(pours,attrib)
    cleanHouse(pours,catlist) 
