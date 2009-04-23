#!/usr/bin/env python
"""
meow_ecoregion_stats.py

Calculate stats on a per-MEOW 2007 ecoregion, in the 0-200m depth zone

Author: Shaun C. Walbridge
""" 

import sys
import os
import math
import glob

def getOpts():
   meow_raster = 'meow_2007_200m_raster'
   meow_vector = 'meow_2007_clipped_200m'
   threat_raster = 'threat_sum_export_clean'
   column = 'ECO_CODE'
   prefix = 'meow_ecoregion'
   return (meow_raster, meow_vector, threat_raster, column, prefix)

def getEnv():
    cmd = "g.gisenv"
    lines = os.popen(cmd).read().rstrip().replace("'","").replace(';','').split("\n")
    env = {}
    for o in [i.split('=') for i in lines]:
        env[o[0]] = o[1]

    return env

def getPath():
    # return raster path
    env = getEnv()
    return "%s/%s/%s/cellhd/" % (env['GISDBASE'],env['LOCATION_NAME'],env['MAPSET'])
    
def generateRandom(input_raster, percent, cell_count):
    random_rname = '%s_%ipct' % (input_raster, percent)

    # randomly select cells of this percentage from the input raster
    cmd = 'r.random in=%s raster_output=%s n=%i' % (input_raster, random_rname, cell_count)
    print cmd
    os.popen(cmd)

    # r.sum returns a line containing 'SUM = 123.45', just grab the number
    cmd = 'r.sum %s' % random_rname
    random_sum = float(os.popen(cmd).read().rstrip().split('=')[1].lstrip())

    return random_sum
             
if __name__ == '__main__':
    (meow_raster, meow_vector, threat_raster, column, prefix) = getOpts()
    # reset region to the default
    cmd = 'g.region -dp'
    os.popen(cmd)

    cmd = 'r.stats -ci %s' % meow_raster
    area_info = os.popen(cmd).read().rstrip().split('\n')
    area_list = [i.split(' ') for i in area_info][:-1]
    #print area_list
    #area_list = [['20002', '33309'], ['20003', '136244'], ['20004', '186227']]

    ecoregion_stats = []
    # process a single element
    for region in area_list:
        (ecoregion, cell_count_str) = region
        cell_count = int(cell_count_str) 

        # extract from the source vector the area with the ecoregion
        vname = '%s_%s' % (prefix, ecoregion)
        rname = '%s_%s_threat' % (prefix, ecoregion)
        cmd = 'v.extract input=%s output=%s where="%s = %s"' % (meow_vector, vname, column, ecoregion)
        os.popen(cmd)

        # set the region to the new vector file
        cmd = 'g.region vect=%s' % vname
        os.popen(cmd)

        # generate a raster containing the threat model values in this ecoregion
        cmd = "r.mapcalc %s='if(%s == %s, %s, null())'" % (rname, meow_raster, ecoregion, threat_raster)
        os.popen(cmd)

        avg_values = []
        # now generate randomizations of this raster
        for i in range(5, 100, 5):
            val = i * 0.01
            random_cell_count = int(val * cell_count)
            random_rname = '%s_%ipct' % (rname, i)

            random_sum = generateRandom(rname, i, random_cell_count)
            avg_values.append([i, random_sum / random_cell_count])
      
        avg_values_str = ["%5s | %5s" % (a, b) for (a, b) in avg_values]
        ecoregion_stats.append([ecoregion, avg_values_str]) 

    #avg_values_str = ["%5s | %5s" % (a, b) for (a, b) in avg_values]
    for (ecoregion, stats) in ecoregion_stats:
        print 'Ecoregion %s' % ecoregion
        print '==============='
        print '%5s | %5s' % ('%', 'value')
        print '------|----------------'
        print '\n'.join(stats)
        print 
