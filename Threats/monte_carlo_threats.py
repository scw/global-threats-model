#!/usr/bin/env python
"""
monte_carlo_threats.py

Creates a new mapset, runs the threat model, calculates model statistics 
for a particular instance of the Monte Carlo simulation, as defined in an
input CSV.

Usage: monte_carlo_threats.py /path/to/model.csv /path/to/grass/location

"""

import os
import re
import sys
import shutil

from os.path import *
from grass_settings import settings

def export_vars(env=None):
    """
    Exports GRASS evnironment variables defined in __init__ function

    Attributes:
        env     -   eventualy dictionary with 'VAR':'VALUE' pares
                    default: env
    """
    for key in env.keys():
        os.environ[key] = env[key]

    # GIS_LOCK
    os.environ['GIS_LOCK']=str(os.getpid())

wind = \
"""\
proj:       99
zone:       0
north:      9020067.3726316
south:      -9020981.82694699
east:       18041068.72414817
west:       -18040095.196132
cols:       38611
rows:       19306
e-w resol:  934.47887701
n-s resol:  934.47887701
top:        1
bottom:     0
cols3:      38610
rows3:      19305
depths:     1
e-w resol3: 934.47887701
n-s resol3: 934.47887701
t-b resol:  1
"""\

# find the range of values
if len(sys.argv) == 3:
    csv_file = sys.argv[1]
    csv_name = splitext(basename(csv_file))[0]
    location = sys.argv[2]
else:
    csv_name = 'artisinal_fishing_model'
    location = '/mnt/storage/marine_threats/grass/world_mask'

mapset = '%s/%s' % (location, csv_name)
cwd = os.getcwd()
# XXX: check for csv existence?
from socket import gethostname
print gethostname()

print mapset
# create new mapset
if not isdir(mapset):
    os.mkdir(mapset)

wf = open("%s/WIND" % mapset, 'w')
wf.write(wind)
wf.close()
os.chdir(mapset)

tempdir = abspath(curdir)
(gisdbase,location_name) = os.path.split(location)
if not location_name:
    (gisdbase,location_name) = os.path.split(os.path.split(location)[0])
grassenv = {
    'LOCATION_NAME' : location_name,
    'MAPSET' : csv_name,
    'GISDBASE' : gisdbase,
    'GRASS_GUI' : 'text',
}

# Update with settings pulled from grass_settings
grassenv.update(settings)

export_vars(grassenv)

# create gisrc
gisrc = open(os.path.join(tempdir,"grass60rc"),"w")
gisrc.write("LOCATION_NAME: %s\n" % (grassenv['LOCATION_NAME']))
gisrc.write("MAPSET: %s\n" % (grassenv['MAPSET']))
gisrc.write("DIGITIZER: none\n")
gisrc.write("GISDBASE: %s\n" % (grassenv['GISDBASE']))
gisrc.write("OVERWRITE: 1\n")
gisrc.write("GRASS_GUI: text\n")
gisrc.close()

export_vars({"GISRC": os.path.join(tempdir,"grass60rc")})

print "Running the threats model.."
# Calculate the threat model
os.chdir(cwd)
cmd = "python threat_model.py %s %s" % (csv_file, csv_name)
handle = os.popen(cmd, 'r', 1)
for line in handle:
      print line,
handle.close()

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
lines = fin.readlines()

pattern = '^[0-9\.]+-([0-9]+\.[0-9]{2})[0-9]+ ([0-9]+)'
for line in lines:
    m = re.search(pattern, line)
    if m:
        fout.write("%s,%s\n" % m.groups())

fin.close()
fout.close()

# copy the CSV to the user's home directory
shutil.copyfile('./%s' % model_csv, '%s/%s' % (os.environ['HOME'], model_csv))

# delete mapset to save on disk
if isdir(mapset):
    shutil.rmtree(mapset)
