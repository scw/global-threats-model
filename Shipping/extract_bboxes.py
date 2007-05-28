#!/usr/bin/env python
"""
 extract_clipped.py

 Extract the shipping data within each 30x15 degree boxes
 
Author: Shaun C. Walbridge
"""

import sys, os, psycopg2

def commit(sql):
    try:
        c.execute(sql)
        # print "inserted %s" % sql
    except:
        conn.rollback()
        print "borked, trying %s" % sql
    conn.commit()

def drop_tables(sql):
    f = open('input/drop_extract_tables.sql', 'w')
    f.writelines(sql)
    f.close()

# connect to PostGIS database
dbc = "dbname=gisdata user=postgres host=localhost"
try:
   conn = psycopg2.connect(dbc)
   c = conn.cursor()
except:
   print "connection to: \"%s\" failed." % dbc
   sys.exit(1)

# create bbox layer from graticule
cmd = "shp2pgsql input/graticule_10x5/grat_10x5.shp shipping_bboxes | psql -d gisdata"
os.popen(cmd)
drop = []
drop.append("DROP TABLE shipping_bboxes;")

# add name column for each bbox, used for creating subtables
c.execute("ALTER TABLE shipping_bboxes ADD COLUMN name text")
sql = """UPDATE shipping_bboxes SET 
            name = 'bbox_' 
            || replace(round(x(centroid(the_geom))),'-','n') || '_' 
            || replace(round(y(centroid(the_geom))), '-', 'n')
      """
c.execute(sql)

c.execute("SELECT name FROM shipping_bboxes")
rows = c.fetchall()

for r in rows:
    name = r[0] # bbox name
    print "inserting table %s" % name

    # get point locations to build linestring
    sql = """CREATE TABLE %s AS
             ( SELECT s.*, intersection(s.the_geom, b.the_geom) AS intersection
               FROM ship_buff_wgs84 s, shipping_bboxes b
               WHERE (overlaps(s.the_geom, b.the_geom) OR
                      contains(b.the_geom, s.the_geom)
                     ) AND b.name = '%s'
             )
          """ % (name, name)
    commit(sql)

    cmd = "pgsql2shp -f 'output/extract_clipped/%s' -g intersection gisdata %s" % (name, name)
    os.popen(cmd)
    
    drop.append("DROP TABLE %s;" % name)

drop_tables(drop)
print "Done."    
