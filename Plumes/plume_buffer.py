#!/usr/bin/env python 
import sys
import os
import math

def getArgs():
    try:
        vectorpours = sys.argv[1]
        attrib = sys.argv[2]
        cutoff = float(sys.argv[3])
        return vectorpours,attrib,cutoff
    except:
        print sys.argv[0] + " usage: <vector name> <attribute> <maximum distance (m)>"
        sys.exit(1)

def getCatList(vector,attrib):
    cmd = "v.db.select -c map=%s column=cat,basin_id,%s" % (vector,attrib)
    lines = os.popen(cmd).read().strip().split('\n')
    catlist = {}
    for i in lines:
        pair = i.split('|')
        catlist[pair[0]] = [pair[1],pair[2]]
    return catlist

def defDecay(vector, attribute, maxDist):
    # find the maximum value within the attribute column
    cmd       = "v.db.select %s col=%s" % (vector, attribute)
    maxstring = os.popen(cmd).read()
    maxlist   = maxstring.strip().split('\n')[1:]
    maxvalue  = max([float(i) for i in maxlist])
    
    decay = float(math.sqrt(maxvalue)/(float(maxDist) + 1))
    return decay    

def cleanHouse(vector,catlist):
    for c in catlist:
        cmd = "g.remove vect=%s_cat%s" % (vector, c)
        os.popen(cmd)
        cmd = "g.remove rast=%s_rast%s,%s_buff_rast%s,cost_cat%s" % \
              (vector, c, vector, c, c)
        os.popen(cmd)

    return True

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
    value_float = float(value)
    value_int = int(value_float)
    # Extract the single point
    cmd = 'v.extract input=%s output=%s_cat%s where="cat = %s" new=%s' % \
           (pours, pours, c, c, value_int)
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

    cmd ="r.buffer input=%s_rast%s out=%s_buff_rast%s distances=3.5 " \
         "units=kilometers" % (pours, c, pours, c)
    os.popen(cmd)

    dw = 'dw_cat' + str(c)
    cost = 'cost_cat' + str(c) 
    plume = 'plume_cat' + str(c)

    # Calculate cost distance
    cmd = "r.cost -k input=ocean max_cost=%s output=%s start_rast=%s_buff_rast%s" % \
          (maxdist, cost, pours, c)
    os.popen(cmd)

    # Mask out non-ocean cells
    cmd = 'r.mapcalc %s = "if( ocean >= 0, %s)"' % (dw,cost) 
    os.popen(cmd)

    # Area Weighted distribution of sediment 
    cmd = 'r.stats -c %s' % dw
    area_info = os.popen(cmd).read().rstrip().split('\n')

    area_list = [i.split(' ') for i in area_info][:-1]

    init = value_float
    pct = 0.005 # percentage of material deposited at each buffer ring
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
            if init == 0:
                break
            print "count: %s init: %i" % (count, init)
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
            debugString.append([dist, count, percell, int(sum), int(remain)])
            reclass_string += "%s = %s\n" % (dist, percell) 

    #log.write("%s\n" % debugString[:10])
    if remain > 1:
        log.write("%s,%s,Possible land-locked pour. Still %s units left to be distributed.\n" % (basin_id,c,remain))
    
    # Reclass the dw map and recreate the plume map
    cmd = "r.reclass input=%s output=%s <<EOF \n%sEOF" % (dw,plume,reclass_string)
    os.popen(cmd)

    # Clean up
    log.flush()

def addPlumes(outputFile):
    cmd = "g.gisenv"
    lines = os.popen(cmd).read().rstrip().replace("'","").replace(';','').split("\n")
    output = [i.split('=') for i in lines]
    path = "%s/%s/%s/cellhd/" % (output[0][1],output[1][1],output[2][1])
    cmd = "ls -1 %s | grep plume_cat" % path
    plumenames = os.popen(cmd).read().strip().split('\n')
    plumes = []
    for pn in plumenames:
        plumes.append(path + pn)

    pl = len(plumes)
    batchcount = 500
    tempids = []
    for i in range(0,pl,batchcount):
        start = i
        end = i + batchcount
        #print plumes[start:end]
        id = "plume" + str(start) + str(end)
        tempids.append(id + ".img")
        cmd = "./gdal_add.py -o %s.img -ot Float32 -of HFA -init 0 %s " % \
              (id, ' '.join(plumes[start:end]) )
        os.popen(cmd)

    cmd = "./gdal_add.py -o %s -ot Float32 -of HFA -init 0 %s " % \
          (outputFile, ' '.join(tempids))
    print "================================================="
    print " Adding all plumes into a single grid"
    print cmd
    os.popen(cmd)

if __name__ == '__main__':
    pours, attrib, maxdist = getArgs()

    catlist = getCatList(pours,attrib)
  
    # create error log file
    logfile = "plume_%s_%s.log" % (pours, attrib)
    log = open(logfile,'w')
    log.write('# plume_buffer log output\n')
    log.write('basin_id,category,message\n')

    i = 1
    for cat in catlist.keys():
        print "========  %s of %s (%s percent) ================" % \
               (i,len(catlist),int(100 * (float(i)/float(len(catlist)))))
        processCategory(cat,catlist[cat][0],catlist[cat][1])
        #log.write("%s,%s,%s\n" % (cat,catlist[cat][0],catlist[cat][1]))
        i = i + 1

    addPlumes("%s_%s_total.img" % (pours, attrib))
    log.close()
