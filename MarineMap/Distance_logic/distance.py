#!/usr/bin/env python
# --------------------------------------------------------------------------------------------------
"""
distance.py
This is a grass module to generate the distances between the centroid of an MPA
and the centroids of all other MPAs.

This function uses the r.cost tool from GRASS 6.3

Authors: Colin M Ebert, Shaun C Walbridge
"""
# --------------------------------------------------------------------------------------------------



import sys
import os
import re
import math
import glob



# --------------------------------------------------------------------------------------------------
#need to import the entire extent for SoCal or whatever region you are working on
# --------------------------------------------------------------------------------------------------

def export_vars(env=None):
    """
    Export GRASS environment variables defined in __init__ function

    Attributes:
        env     -   eventually dictionary with 'VAR':'VALUE' pares
                    default: env

    """
    for key in env.keys():
        os.envoron[key] = env[key]

        #GIS_LOCK
        os.environ['GIS_LOCK']=str(os.getpid())


wind = \
"""\
proj:       99
zone:       0
north:      -393050.5
south:      -605050.5
west:       -49206.59
east:       273293.41
cols:       2120
rows:       3225
e-w resol:  100
n-s resol:  100
top:        1
bottom:     0
cols3:      2120
rows3:      3225
depths:     1
e-w resol3: 100
n-s resol3: 100
t-b resol:  1
"""\

# --------------------------------------------------------------------------------------------------
#need to import centroid of originating MPA
# --------------------------------------------------------------------------------------------------




# --------------------------------------------------------------------------------------------------
#run r.cost function on imported MPA for entire region
# this should look something like:
# r.cost -k input=extent_100m_nodata output=cost_9_10_ns start_points=point_9  max_cost=0 percent_memory=100 --overwrite
# the output name should be something based upon the originating id and a timestamp
# --------------------------------------------------------------------------------------------------




# --------------------------------------------------------------------------------------------------
# Need to add column to point layer for value of cost path matrix
# should look like:
# v.db.addcol map=point_8 layer=1 'columns=cost_9_8 DOUBLE' 
# --------------------------------------------------------------------------------------------------





# --------------------------------------------------------------------------------------------------
#   need to intersect all other MPA centroids that are applicable with this output layer to get a distance
#       value in cumulative 100m cells.  This data should be stored and output into the originating
#       centroids attribuite field inside a new table.
#   should look like:
# v.what.rast vector=point_8 raster=cost_9_8 layer=1 column=cost_9_8 
# --------------------------------------------------------------------------------------------------



