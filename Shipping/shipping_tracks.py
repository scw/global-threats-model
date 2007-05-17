#!/usr/bin/env python
"""
 shipping_tracks.py

 Merge shipping points into tracks using PostGIS.
 
Author: Shaun C. Walbridge
"""

import sys, math, psycopg2

def commit(sql):
    try:
        c.execute(sql)
        #print "inserted %s" % id
    except:
        conn.rollback()
        print "borked, trying %s" % sql
    conn.commit()

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
    dates = []

    # get point locations to build linestring
    sql = """SELECT lon, lat, date 
             FROM shipping_clean 
             WHERE id = '%s' 
             ORDER BY date """ % id
    c.execute(sql)
    q = c.fetchall()
    count = len(q)

    if count is 1:
        # only one sounding, capture as a point
        (lon, lat, date) = q.pop()
        sql = """INSERT INTO ship_points
                 VALUES('%s', '%s',
                   GeometryFromText('POINT(%s)', 4326))
              """ % (id, date, "%s %s" % (lon, lat))
        commit(sql)

    else:
        # multiple soundings, capture linestrings
        (prev_lon, prev_lat, prev_date) = q[0]
        for point_row in q:
            # check for dateline 'wrapping'
            (cur_lon, cur_lat, cur_date) = point_row
            if abs(cur_lon - prev_lon) > 180 and \
               str(cur_lon * prev_lon)[0] is '-':
                # interpolate two points at the anti-meridian boundry

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
                p = [ ("%s %s"        % (prev_lon, prev_lat), prev_date), \
                      ("%3.9f %2.10f" % (prev_s, s_lat),      prev_date), \
                      ("%3.9f %2.10f" % (cur_s, s_lat),       cur_date),  \
                      ("%s %s"        % (cur_lon, cur_lat),   cur_date) ]
                geom += p # add these points to the queue

            else:
                # push lon lat pair onto geom
                geom.append(('%s %s' % (cur_lon, cur_lat), cur_date))

            # set lat / lon for next run
            (prev_lon, prev_lat, prev_date) = point_row

        (p_lonlat, p_date) = geom[0]
        for g in geom:
            (c_lonlat, c_date) = g
            # skip the anti-meridian line
            cs = c_lonlat.strip('-')
            ps = p_lonlat.strip('-')
            
            if cs != ps:
                sql = """INSERT INTO ship_lines2 VALUES('%s', %i, '%s', '%s',
                           GeometryFromText('LINESTRING(%s, %s)', 4326))
                      """ % (id, count, p_date, c_date,  p_lonlat, c_lonlat)
                commit(sql)
            else:
                if cs[:3] == '180':
                    print "Skipping anti-meridian case: %s to %s" % (p_lonlat, c_lonlat)
                else:
                    sql = """INSERT INTO ship_points
                             VALUES('%s', '%s',
                               GeometryFromText('POINT(%s)', 4326))
                          """ % (id, c_date, c_lonlat)
                    commit(sql)        
            (p_lonlat, p_date) = g

print "Done."    
