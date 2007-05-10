#!/usr/bin/env python
"""
 shipping_tracks.py

 Merge shipping points into tracks using PostGIS.
 
Author: Shaun C. Walbridge
"""

import sys, math, psycopg2

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

    (prev_lon, prev_lat) = q[0]
    for point in q:
        # check for dateline 'wrapping'
        (cur_lon, cur_lat) = point
        if abs(cur_lon - prev_lon) > 180 and \
           str(cur_lon * prev_lon)[0] is '-':
            # interpolate two points at the 180/-180 boundry

            cur_s, prev_s = 180, 180 # signs for longitude at boundry
            if prev_lon < 0:
                p_lon = prev_lon + 360
                prev_s *= -1
            else:
                p_lon = prev_lon
            if cur_lon < 0:
                c_lon = cur_lon + 360
                cur_s *= -1
            else:
                c_lon = cur_lon
            slope = (prev_lat - cur_lat)/(p_lon - c_lon)
            s_lat = slope*(180 - p_lon) + prev_lat
            
            # generate new points based on bountry split
            p = "%s %s,%3.9f %2.10f),(%3.9f %2.10f,%s %s" % \
                (prev_lon, prev_lat, prev_s, s_lat, cur_s, s_lat, cur_lon, cur_lat)
            geom.append(p)

        else:
            # push lon lat pair onto geom
            geom.append('%s %s' % point)
        # set lat / lon for next run
        (prev_lon, prev_lat) = point

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
                   GeometryFromText('MULTILINESTRING((%s))', 4326)) 
              """ % (id, count, date_min, date_max, ','.join(geom))
    try:
        c.execute(sql)
        print "inserted %s" % id
    except:
        conn.rollback()
        print "borked, trying %s" % sql
    conn.commit()

print "Done."    
