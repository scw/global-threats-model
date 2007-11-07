#!/usr/bin/env python
"""
histogram.py

Extracted from monte_carlo_threats.py, this just runs the histogram component within
a current mapset against the specified raster. The current extent is expected to match
the region of interest.

Usage: histogram.py grass_raster_name

"""

import os
import re
import sys
import shutil

from os.path import *

csv_name = sys.argv[1]

# Calculate the statistics for the resulting threat model
cmd = 'r.info -r %s' % csv_name
maxmin = os.popen(cmd).read().split()
for v in maxmin:
    (var, val) = v.split("=")
    exec "%s = %s" % (var, val)

range = max - min
# bins are of size .01
bins = int(range * 100)

cmd = "r.stats -c -C %s nsteps=%i output=%s.txt" % (csv_name, bins, csv_name)
os.popen(cmd)

model_csv = '%s.csv' % csv_name

fin = open('%s.txt' % csv_name, 'r')
fout = open(model_csv, 'w')
flog = open('%s.log' % csv_name, 'w')
lines = fin.readlines()

pattern = '^[0-9\.]+-([0-9]+\.[0-9]{2})[0-9]+ ([0-9]+)'
# store the running totals of pixels and cummulative value
pixel_count = 0
sum_count = 0

for line in lines:
    m = re.search(pattern, line)
    if m:
        bin_in, count_in = m.groups()
        bin = float(bin_in)
        count = int(count_in)
        # ignore the first bin, it contains our zero values
        if bin_in != '0.01':
            pixel_count += count
            sum_count += bin * count
        fout.write("%s,%s\n" % (bin, count))

flog.write("pixel count: %s\ncummulative sum: %s\n" % (pixel_count, sum_count))
fin.close()
fout.close()
flog.close()

# copy the CSV to the user's home directory
shutil.copyfile('./%s' % model_csv, '%s/%s' % (os.environ['HOME'], model_csv))

