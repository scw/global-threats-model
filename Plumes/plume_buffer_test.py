#!/usr/bin/env python 
import sys
import os
import math

from plume_buffer import getArgs, getCatList, defDecay
def processCategory(c,basin_id,value):
    global log
    global pours, attrib, maxdist
    print
    print " Processing category ", c
    print
    log.write("%s,%s,%s\n" % (c, basin_id, value))
    if value == '0':
        log.write("%s has a value of 0, skipping.\n" % basin_id)
        log.flush()
        return
    
    cmd = 'g.region rast=ocean'
    os.popen(cmd)

    value = float( value )
     
    # Extract the single point
    cmd = 'v.extract input=%s output=%s_cat%s where="cat = %s" new=%s' % \
           (pours, pours, c, c, int(value))    
    os.popen(cmd)

    # subset region down to the widest possible buffer map
    cmd = "g.region vect=%s_cat%s align=ocean" % (pours,c)
    os.popen(cmd)

    cmd = "g.region -gp"
    regionsplit = os.popen(cmd).read().rstrip().split('\n')
    region = {}
    for r in regionsplit:
       pv = r.strip().split('=')
       if (pv[0] != ''):
           region[pv[0]] = float(pv[1]) 
    n = region['n'] + maxdist
    s = region['s'] - maxdist
    w = region['w'] - maxdist
    e = region['e'] + maxdist
    cmd = "g.region n=%s s=%s w=%s e=%s align=ocean" % (n,s,w,e)
    os.popen(cmd)

    # Convert to raster 
    cmd = "v.to.rast input=%s_cat%s output=%s_rast%s use=cat" % \
           (pours, c, pours, c)    
    os.popen(cmd)

    dw = 'dw_cat' + str(c)
    cost = 'cost_cat' + str(c) 
    plume = 'plume_cat' + str(c)

    # Calculate cost distance
    cmd = "r.cost -k input=ocean_sub max_cost=%s output=%s start_rast=%s_rast%s" % \
          (maxdist, cost, pours, c) 
    os.popen(cmd)
    #print cmd

    # Mask out non-ocean cells
    cmd = 'r.mapcalc %s = "if( ocean >= 0, %s)"' % (dw,cost) 
    os.popen(cmd)

    # Area Weighted distribution of sediment 
    cmd = 'r.stats -c %s' % dw
    area_info = os.popen(cmd).read().rstrip().split('\n')
    #print area_info
    area_list = [i.split(' ') for i in area_info][:-1]

    init = float(value)
    pct = 0.002 # percentage of material deposited at each buffer ring
    reclass_string = ""

    listlen = len(area_list)

    sum = 0
    percell = 0
    remain = 0
    debugString = []

    if listlen == 0:
        log.write("%s,%s,Area list is zero length, all values are null.\n" % (basin_id,c))
        return

    for (dist,count) in area_list:
        percell = init * pct
        sum = percell * float(count)
        remain = init - sum
        if remain < 0:
            remain = 0
            percell = init / float(count)
            sum = init
        init = remain
        percell = int(round(percell))
        # if the pour would be empty, force all the values to the first distance
        if (dist == '1' and percell == 0):
            percell = int(float(count)/init)
            if percell > 0:
                log.write("%s hits empty at dist one, assigning %i to dist one.\n" % (basin_id, percell))
                reclass_string = "%s = %s\n" % (dist, percell)
                remain = 0
            else:
                log.write("%s too small at dist one, move along.\n" % basin_id)
                return
            break
        else:
            if (dist == '1'):
                debugString.append('unrounded value at dist 1: %2f' % (init * pct))
            debugString.append([dist, count, percell, int(sum), int(remain)])
            reclass_string += "%s = %s\n" % (dist, percell) 

    log.write("%s\n" % debugString[:10])
    if remain > 1:
        log.write("%s,%s,Possible land-locked pour. Still %s units left to be distributed.\n" % (basin_id,c,remain))
    log.flush()

if __name__ == '__main__':
    pours, attrib, maxdist = getArgs()

    catlist = getCatList(pours,attrib)
  
    # create error log file
    logfile = "plume_%s_%s_test.log" % (pours, attrib)
    log = open(logfile,'w')
    log.write('# plume_buffer log output\n')
    log.write('basin_id,category,message\n')

    i = 1
    for cat in catlist.keys():
        print "========  %s of %s (%s percent) ================" % \
               (i,len(catlist),int(100 * (float(i)/float(len(catlist)))))
        processCategory(cat,catlist[cat][0],catlist[cat][1])
        i = i + 1

    log.close()
