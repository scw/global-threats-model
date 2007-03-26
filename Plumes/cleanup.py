#!/usr/bin/env python 
import sys
import os
import math

from plume_buffer import getCatList, cleanHouse, getArgs

if __name__ == '__main__':
    pours, attrib = getArgs()

    catlist = getCatList(pours,attrib)
    cleanHouse(pours,catlist) 
