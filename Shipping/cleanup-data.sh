#!/usr/bin/env bash
# cleanup-data.sh
# Remove all buoy data from shipping dataset
# Run as the postgres user or with a .pgpass file

# Import the data into PostGIS
shp2pgsql -d input/mw_shipping/xbt_r05all_point.shp shipping | psql -d gisdata

# Strip the bad data from our table (verified buoy data)
psql gisdata < input/buoys.sql

# Add necessary tables for data cleanup (line, point tables)
psql gisdata < input/cleanup.sql

# Run python code to process ship tracks into line segments
# dumps results into two tables:
# ship_lines, ship_points
python shipping_tracks.py

# Dump the results to a new shapefile
pgsql2shp -f output/shipping-lines.shp gisdata ship_lines
pgsql2shp -f output/shipping-points.shp gisdata ship_points
cp "output/WGS 1984.prj" output/shipping-lines.prj
cp "output/WGS 1984.prj" output/shipping-points.prj
