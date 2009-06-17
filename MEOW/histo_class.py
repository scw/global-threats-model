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

def calculate_histogram(bins, raster, basename, stats = False):
    cmd = "r.stats -c -C %s nsteps=%i output=%s.txt" % (raster, bins, basename)
    os.popen(cmd)

    fin = open('%s.txt' % basename, 'r')
    fout = open('%s.csv' % basename, 'w')
    if stats:
        flog = open('%s.log' % basename, 'w')
        # store the running totals of pixels and cummulative value
        pixel_count = 0
        sum_count = 0

    pattern = '^[0-9\.]+-([0-9]+\.[0-9]{2})[0-9]+ ([0-9]+)'
    lines = fin.readlines()

    for line in lines:
        m = re.search(pattern, line)
        if m:
            bin_in, count_in = m.groups()
            bin = float(bin_in)
            count = int(count_in)
            if stats:
                pixel_count += count
                sum_count += bin * count
            fout.write("%s,%s\n" % (bin, count))

    if stats:
        flog.write("pixel count: %s\ncummulative sum: %s\n" % (pixel_count, sum_count))
        flog.close()

    fin.close()
    fout.close()

def calculate_range(raster):
    cmd = 'r.info -r %s' % raster 
    maxmin = os.popen(cmd).read().split()
    for v in maxmin:
        (var, val) = v.split("=")
        exec "%s = %s" % (var, val)

    range = max - min
    return range
