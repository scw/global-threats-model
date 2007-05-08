#!/usr/bin/env bash
# cleanup-data.sh
# Remove all buoy data from shipping dataset
# Run as the postgres user or with a .pgpass file

# Make sure the Mollweide Projection is in PostGIS
#psql gisdata < input/mollweide.sql

# Import the data into PostGIS
#shp2pgsql -d input/mw_shipping/xbt_r05all_point.shp shipping | psql -d gisdata

# Strip the bad data from our table (verified buoy data)
#psql gisdata < input/buoys.sql

# Dump the results to a new shapefile
pgsql2shp -f output/shipping-lines.shp gisdata ship_lines
pgsql2shp -f output/shipping-points.shp gisdata ship_points
