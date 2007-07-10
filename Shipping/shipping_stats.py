#!/usr/bin/env python
"""
 shipping_stats.py

 Get some basic shipping statistics 
 
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
points = 0
ships  = 0

for row in r:
    # get point locations of valid ship tracks
    id = row[0]
    sql = """SELECT id
             FROM shipping_clean 
             WHERE id = '%s'
          """ % id
    c.execute(sql)
    q = c.fetchall()
    count = len(q)

    if count > 1:
        points += count
        ships += 1

print "Total ships included:  %10i" % ships
print "Total points included: %10i" % points
