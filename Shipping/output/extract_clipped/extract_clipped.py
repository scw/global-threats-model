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

# connect to PostGIS database
connect():
    dbc = "dbname=gisdata user=postgres host=localhost"
    try:
        conn = psycopg2.connect(dbc)
        return conn.cursor()
    except:
        print "connection to: \"%s\" failed." % dbc
        sys.exit(1)


# create bbox layer from graticule

c = connect()
c.execute("SELECT name FROM shipping_bboxes")
rows = c.fetchall()

for r in rows:
    name = r[0] # bbox name
    table = "bbox_%s" % name
    print "inserting table %s" % table

    # get point locations to build linestring
    sql = """CREATE TABLE %s AS
             ( SELECT s.*, intersection(s.the_geom, b.the_geom) AS intersection
               FROM ship_buff_wgs84 s, shipping_bboxes b
               WHERE (overlaps(s.the_geom, b.the_geom) OR
                      contains(b.the_geom, s.the_geom)
                     ) AND b.name = '%s'
             )
          """ % (table, name)
    commit(sql)

    cmd = "pgsql2shp -g intersection gisdata %s" % table
    os.popen(cmd)

print "Done."    
