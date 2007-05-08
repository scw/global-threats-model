#!/usr/bin/env python
"""
 shipping_tracks.py

 Merge shipping points into tracks using PostGIS.
 
Author: Shaun C. Walbridge
"""

import sys, psycopg2

# connect to PostGIS database
dbc = "dbname=gisdata user=postgres host=localhost"
try:
    conn = psycopg2.connect(dbc)
    c = conn.cursor()
except:
    print "connection to: \"%s\" failed." % dbc
    sys.exit(1)


c.execute("SELECT id FROM shipping_clean GROUP BY id")
r = c.fetchall()

for row in r:
    id = row[0] # ship track id
    geom = []

    # get point locations to build linestring
    sql = """SELECT lon, lat
             FROM shipping_clean 
             WHERE id = '%s'
             ORDER BY date
          """ % id
    c.execute(sql)
    q = c.fetchall()
    count = len(q)

    for point in q:
        # push lon lat pair onto geom
        geom.append('%s %s' % point)

    # get the date range so we have an idea of sampling frequency
    sql = """SELECT MAX(date) AS max, MIN(date) AS min
             FROM shipping_clean
             WHERE id = '%s'
          """ % id
    c.execute(sql)
    (date_max, date_min) = c.fetchone()
    
    if count is 1:
        # only one sounding, capture as a point
        sql = """INSERT INTO ship_points VALUES('%s', '%s',
                   GeometryFromText('POINT(%s)', 4326))
              """ % (id, date_max, geom.pop())
    else:
        # multiple soundings, capture linestring
        sql = """INSERT INTO ship_lines VALUES('%s', %i, '%s', '%s', 
                   GeometryFromText('LINESTRING(%s)', 4326)) 
              """ % (id, count, date_min, date_max, ','.join(geom))
    try:
        c.execute(sql)
        print "inserted %s" % id
    except:
        conn.rollback()
    conn.commit()

print "Done."    
