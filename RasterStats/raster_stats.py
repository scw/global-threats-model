#!/usr/bin/python
"""
 Raster Stats
 raster_stats.py

 Extracts raster stats by polygon using system calls to starspan
 Then joins the statistics into a single table in postgresql database

 Note that since a db password is required (but not hardcoded here for good reason)
 you must have a ~/.pgpass file with 0600 permissions whose contents read:
   hostname:port:database:username:password 
"""

import os, sys, psycopg2

debug = False
if debug:
   print "DEBUG MODE.. nothing will happen"

try:
    continent = sys.argv[1]
    db = sys.argv[2]
except:
    print "raster_stats.py [continent-abbreviation] [database-name]*"
    print " * [database-name] must already exist and have postgis and discrete_pivot functions"
    print 
    print " Make sure to edit the options that are hardcoded in this script !!"
    sys.exit(1) 


options = {'starspanBin':  "/usr/local/bin/starspan",
           'outputDir':    "/mnt/storage/marine_threats/work/raster_stats/outputs/%s" % continent,
           'outshpDir':    "/mnt/storage/marine_threats/work/raster_stats/outshp/%s" % continent,
           'tablePrefix':  continent,
           'db':           db,
           'rasterPath':   "/mnt/storage/marine_threats/work/raster_stats/rasters",
           'vectorPath':   "/mnt/storage/marine_threats/work/raster_stats/vectors/basins",
           'connection':   "dbname=%s user=perry host=localhost" % db}

# Set up postgis connection
try:
    conn = psycopg2.connect(options['connection'])
    c = conn.cursor()
except:
    print "Can't Make Postgres Connection!"
    print options['connection']
    print """
 Note that since a db password is required (but not hardcoded here for good reason)
 you must have a ~/.pgpass file with 0600 permissions whose contents read:
   hostname:port:database:username:password 
"""
    sys.exit(1)

def getDiscreteRasters(options):

    igbp = {'path':       "%s/igbp/%s_igbp/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'igbp',
            'band':       1 }

    glwd = {'path':       "%s/glwd/%s_glwd/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'glwd',
            'band':       1 }

    soil = {'path':       "%s/soil/%s_soil.tif" % (options['rasterPath'],options['tablePrefix']),
            'name':       'soil',
            'band':       1 }

    iucn ={'path':       "%s/iucn/%s_iucn/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'iucn',
            'band':       1 }

    drl = [igbp,soil,glwd,iucn]
    return drl

def getContinuousRasters(options):
    # Name should be < 6 chars in case dbf is created!!
    wb =   {'path':       "%s/wb/%s_wb.img" % (options['rasterPath'],options['tablePrefix']),
            'name':       'wb',
            'stats':      'avg sum',
            'band':       1 }

    tc =   {'path':       "%s/tc/%s_tc/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'trcov',
            'stats':      'avg min max',
            'band':       1 }

    ferta ={'path':       "%s/ferta/%s_ferta/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'ferta',
            'stats':      'avg min max',
            'band':       1 }

    fertb ={'path':       "%s/fertb/%s_fertb/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'fertb',
            'stats':      'avg min max',
            'band':       1 }

    fertc ={'path':       "%s/fertc/%s_fertc/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'fertc',
            'stats':      'avg sum',
            'band':       1 }

    pesta ={'path':       "%s/pesta/%s_pesta/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'pesta',
            'stats':      'avg min max sum',
            'band':       1 }

    pestb ={'path':       "%s/pestb/%s_pestb/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'fertb',
            'stats':      'avg min max sum',
            'band':       1 }

    pestc ={'path':       "%s/pestc/%s_pestc/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'pestc',
            'stats':      'avg min max sum',
            'band':       1 }

    irr =   {'path':       "%s/irr/%s_irr/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'irr',
            'stats':      'avg min max stdev',
            'band':       1 }

    rusle = {'path':       "%s/rusle/%s_rusle/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'rusle',
            'stats':      'sum min max stdev',
            'band':       1 }

    rusle2 = {'path':       "%s/rusle2/%s_rusle2.img" % (options['rasterPath'],options['tablePrefix']),
            'name':       'rusl2',
            'stats':      'avg sum min max stdev',
            'band':       1 }

    k     = {'path':       "%s/k/%s_k.tif" % (options['rasterPath'],options['tablePrefix']),
            'name':       'k',
            'stats':      'avg median min max stdev',
            'band':       1 }

    glac = {'path':       "%s/glac/%s_glac/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'glac',
            'stats':      'avg sum',
            'band':       1 }

    srtm = {'path':       "%s/srtm/%s_srtm.vrt" % (options['rasterPath'],options['tablePrefix']),
            'name':       'srtm',
            'stats':      'avg min max stdev median',
            'band':       1 }

    footp ={'path':       "%s/footp/%s_footp/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'footp',
            'stats':      'avg min max median stdev',
            'band':       1 }


    resdp ={'path':       "%s/resdp/%s_resdp/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'resdp',
            'stats':      'avg sum',
            'band':       1 }

    treecv ={'path':       "%s/treecv/%s_treecv/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'treecv',
            'stats':      'avg min max median',
            'band':       1 }

    soildeg ={'path':       "%s/soildeg/%s_soildeg/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'soildg',
            'stats':      'avg min max median',
            'band':       1 }

    wild ={'path':       "%s/wild/%s_wild/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'wild',
            'stats':      'avg sum',
            'band':       1 }

    temp ={'path':       "%s/temperature_rst/%s_temperature_rst.img" % (options['rasterPath'],options['tablePrefix']),
            'name':       'temp',
            'stats':      'avg median stdev min max',
            'band':       1 }

    tempr ={'path':       "%s/temprange_rst/%s_temprange_rst.img" % (options['rasterPath'],options['tablePrefix']),
            'name':       'temprg',
            'stats':      'avg median min max',
            'band':       1 }

    wetdays ={'path':       "%s/wetdays_rst/%s_wetdays_rst.img" % (options['rasterPath'],options['tablePrefix']),
            'name':       'wetdy',
            'stats':      'avg median stdev min max',
            'band':       1 }

    pet ={'path':       "%s/pet_rst/%s_pet_rst.img" % (options['rasterPath'],options['tablePrefix']),
            'name':       'pet',
            'stats':      'avg median sum min max',
            'band':       1 }

    precip ={'path':       "%s/precip_rst/%s_precip_rst.img" % (options['rasterPath'],options['tablePrefix']),
            'name':       'prec',
            'stats':      'avg median sum min max',
            'band':       1 }

    humidity ={'path':       "%s/humidity_rst/%s_humidity_rst.img" % (options['rasterPath'],options['tablePrefix']),
            'name':       'humid',
            'stats':      'avg median min max',
            'band':       1 }

    slope ={'path':       "%s/slope/%s_slope.img" % (options['rasterPath'],options['tablePrefix']),
            'name':       'slope',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl1992 ={'path':       "%s/lights_1992/%s_nl1992/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl1992',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl1993 ={'path':       "%s/lights_1993/%s_nl1993/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl1993',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl1994 ={'path':       "%s/lights_1994/%s_nl1994/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl1994',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl1995 ={'path':       "%s/lights_1995/%s_nl1995/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl1995',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl1996 ={'path':       "%s/lights_1996/%s_nl1996/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl1996',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl1997 ={'path':       "%s/lights_1997/%s_nl1997/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl1997',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl1998 ={'path':       "%s/lights_1998/%s_nl1998/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl1998',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl1999 ={'path':       "%s/lights_1999/%s_nl1999/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl1999',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl2000 ={'path':       "%s/lights_2000/%s_nl2000/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl2000',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl2001 ={'path':       "%s/lights_2001/%s_nl2001/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl2001',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl2002 ={'path':       "%s/lights_2002/%s_nl2002/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl2002',
            'stats':      'avg median stdev min max',
            'band':       1 }

    nl2003 ={'path':       "%s/lights_2003/%s_nl2003/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'nl2003',
            'stats':      'avg median stdev min max',
            'band':       1 }

    impervious ={'path':       "%s/impervious/%s_impv/hdr.adf" % (options['rasterPath'],options['tablePrefix']),
            'name':       'impervious',
            'stats':      'avg median stdev min max',
            'band':       1 }    

    crl = [wb, fertc, srtm, rusle, rusle2, k, glac, pestc, treecv, footp, \
           resdp, soildeg, wild, temp, tempr, wetdays, pet, precip, \
           humidity, slope, irr]
    return crl

def getVectors(options):
    # basin_id field MUST exist in both the pour point and the basins
    basins = {'path':  "%s/%s_basins.shp" % (options['vectorPath'],options['tablePrefix']),
             'pourpath':  "%s/%s_pours.shp" % (options['vectorPath'],options['tablePrefix']),
             'name':     'bsn',
             'pourname':     'pour',
             'idfield':  'basin_id'} 

    gtn =   {'path':    "%s/%s_gtn.shp" % (options['vectorPath'],options['tablePrefix']),
             'name':    'gtn',
             'idfield': 'ID_'} 

    vl = [basins]
    return vl

def makeContinuousCmd(r,v,options):
    output = os.path.join(options['outputDir'], \
                          options['tablePrefix']+'_'+v['name']+'_'+r['name']+'.csv' )
    cmd = "%s --vector %s --raster %s --fields %s --stats %s %s" % \
           (options['starspanBin'], v['path'], r['path'], v['idfield'], output, r['stats'])
    return cmd

def makeDiscreteCmd(r,v,options):
    output = os.path.join(options['outputDir'], \
                options['tablePrefix']+'_discrete_'+v['name']+'_'+r['name']+'.csv' )
    cmd = "%s --vector %s --raster %s --count-by-class %s " \
              % (options['starspanBin'], v['path'], r['path'], output)
    return cmd

def makeDiscreteSql(c,r,v,options):
    tablename = options['tablePrefix']+'_discrete_'+v['name']+'_'+r['name']

    # Create New Table
    c.execute("CREATE TABLE %s (fid integer, class integer, count integer);\n\n" \
                % tablename)

    # Read csv file and insert into postgis table    
    infile = options['outputDir'] + '/' + tablename + '.csv'
    fh = open(infile, 'r')
    
    # Skip the first row - the header
    line = fh.readline()
    
    line = fh.readline()
    while line:
        cleanline = line.replace('\n','')
        cols = cleanline.split(',')
    
        sql = "INSERT INTO %s VALUES (%s,%s,%s)" \
              % (tablename, cols[0], cols[1], cols[2]) 
    
        c.execute(sql)
        line = fh.readline()
    
    # Should really have a check here to make sure everything went smooth
    c.connection.commit()
    fh.close()

    # Create percentage table
    sql = """CREATE TABLE %s_%s_%s AS (
       SELECT t.fid AS fid, t.class as class, t.count as count, s.total as total,
         (t.count::numeric / s.total::numeric) * 100 AS percentage
       FROM %s t,
         (SELECT fid, sum(count) AS total
          FROM %s
	  GROUP BY fid) as s
       WHERE t.fid = s.fid );
""" % (options['tablePrefix'],v['name'],r['name'],tablename,tablename)
 
    try:
        c.execute(sql)
        c.connection.commit()
    except:
        c.connection.rollback()
        print 
        print "Creating catagorical percentage table FAILED for %s " % r['name']
        print 

    # Run the pivot table to create 
    # one feature per row, one column w/percentage per class 
    #c.execute("\n\nSELECT discrete_pivot('%s_join','%s_%s_%s','%s');" % \
    #        (options['tablePrefix'],options['tablePrefix'],v['name'],r['name'],r['name']) )


def makeContinuousSql(c,r,v,options):
    # Create new table with proper column names
    sql = "CREATE TABLE %s_%s_%s (fid_%s integer, id_%s text, pix_%s integer" % \
           (options['tablePrefix'],v['name'],r['name'],r['name'],r['name'],r['name']) 
    statcols = r['stats'].split(' ')
    colstring = "fid_%s, id_%s, pix_%s" % (r['name'],r['name'],r['name'])
    for col in statcols:
        column = ', ' + col[:3] + '_' + r['name']
        colstring += column
        sql += column + ' numeric'
    sql += ")"
    try:
        c.execute(sql)
        c.connection.commit()
    except:
        c.connection.rollback()
        print 
        print "Creating continuous raster table FAILED for %s " % r['name']
        print 

    # Read from csv file and insert rows into postgis
    infile = "%s/%s_%s_%s.csv" % \
             (options['outputDir'],options['tablePrefix'],v['name'],r['name'])
    fh = open(infile, 'r')
    
    # Skip the first row - the header
    line = fh.readline()
    
    line = fh.readline()
    while line:
        cleanline = line.replace('\n','')
        cols = cleanline.split(',')
    
        sql = "INSERT INTO %s_%s_%s (%s) VALUES (%s, '%s'" % \
          (options['tablePrefix'], v['name'], r['name'], colstring, cols[0],cols[1])
    
        for i in range(2,len(cols)):
            # There shouldn't be any strings from here on out 
            if cols[i] == 'nan':
                sql += ", Null" 
            else:
                sql += ", %s" % cols[i]
    
        sql += ")"
        #print sql
    
        c.execute(sql)
        
        line = fh.readline()
    
    # Should really have a check here to make sure everything went smooth
    c.connection.commit()
    fh.close()
    

def makeJoinSql(c,cr,v,options):
    # create a 'master table' and join the continuous rasters  

    c.execute("ALTER TABLE %s_%s ADD column fid integer" % \
              (options['tablePrefix'], v['name']) )

    c.execute("UPDATE %s_%s SET fid = gid - 1" % \
              (options['tablePrefix'], v['name']) )

    c.connection.commit()

    tablelist = []
    for r in cr:
        tablelist.append("%s.*" % r['name'] )
    tablenames = ', '.join(tablelist)

    sql = """CREATE TABLE %s_join AS (
      SELECT feature.%s as id_join, feature.fid as fid_join, %s
      FROM %s_%s feature """ % \
       (options['tablePrefix'], v['idfield'], tablenames , options['tablePrefix'],v['name'])

    for r in cr:
        sql += "LEFT JOIN %s_%s_%s %s ON ( feature.%s = %s.id_%s ) \n" % \
         (options['tablePrefix'],v['name'],r['name'],r['name'],v['idfield'],r['name'],r['name'])
    
    sql += ")"

    #print sql
    try:
        c.execute(sql)
        c.connection.commit()
        return 0
    except:
        c.connection.rollback()
        print "Join did not go so well"
        return 1


def importShp(v,options):
    # import the basins shapfile
    cmd = "shp2pgsql -D %s %s_%s | psql -d %s -h localhost -U perry" % \
          (v['path'],options['tablePrefix'],v['name'],options['db'])
    #print cmd
    os.system(cmd)

    # import the pour points shapfile
    cmd = "shp2pgsql -D %s %s_%s | psql -d %s -h localhost -U perry" % \
          (v['pourpath'],options['tablePrefix'],v['pourname'],options['db'])
    #print cmd
    os.system(cmd)

    return 0

def makePivotSql(c,dr,v,options):
    # Pivot the discrete tables and join to master table
    for r in dr:
        c.execute("SELECT discrete_pivot('%s_join','%s_%s_%s','%s')" % \
          (options['tablePrefix'],options['tablePrefix'],v['name'],r['name'],r['name']) ) 
    c.connection.commit()
    return 0

def createViews(v,options):
    # Create polygon view of basins
    sql = """
      CREATE VIEW %s_%s_polyview AS (
        SELECT * from %s_join, %s_%s where %s_%s.%s = %s_join.id_join
      ) """ % \
    (options['tablePrefix'],v['name'],options['tablePrefix'],options['tablePrefix'],v['name'], \
     options['tablePrefix'],v['name'],v['idfield'],options['tablePrefix'] )
    
    c.execute(sql)

    # Create point view of pour points
    sql = """
      CREATE VIEW %s_%s_pointview AS (
        SELECT * from %s_join, %s_%s where %s_%s.%s = %s_join.id_join
      ) """ % \
    (options['tablePrefix'],v['name'],options['tablePrefix'],options['tablePrefix'],v['pourname'], \
     options['tablePrefix'],v['pourname'],v['idfield'],options['tablePrefix'] )
    
    c.execute(sql)
    
    c.connection.commit()

def exportViews(v,options):
    # export the pour points 
    cmd = "pgsql2shp -f %s/%s_%s_pointview.shp %s %s_%s_pointview" % \
          (options['outshpDir'],options['tablePrefix'], v['name'], options['db'], \
           options['tablePrefix'], v['name'])
    #print cmd
    os.system(cmd)

    # export the basins 
    cmd = "pgsql2shp -f %s/%s_%s_polyview.shp %s %s_%s_polyview" % \
          (options['outshpDir'],options['tablePrefix'], v['name'], options['db'], \
           options['tablePrefix'], v['name'])
    #print cmd
    os.system(cmd)


# ========================================================#
#           MAIN
if __name__ == '__main__':
    dr = getDiscreteRasters(options)
    cr = getContinuousRasters(options)
    vl = getVectors(options)

    for v in vl:
        if dr:
            for r in dr:
                cmd = makeDiscreteCmd(r,v,options)
                print "Processing %s ..." % r['name']
                os.system(cmd)
                makeDiscreteSql(c,r,v,options)

        if cr:
            for r in cr:
                cmd = makeContinuousCmd(r,v,options)
                print "Processing %s ..." % r['name']
                os.system(cmd)
                makeContinuousSql(c,r,v,options)

        importShp(v,options)
        makeJoinSql(c,cr,v,options)
        makePivotSql(c,dr,v,options)
        createViews(v,options)
        exportViews(v,options)

    c.connection.close()
