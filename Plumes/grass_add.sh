#
# GRASS Script to add all plumes into a single output raster
# DEPRECATED! Use gdal_add.py instead
#

g.mlist type=rast pattern=plume_* > plume_raster.list
g.region rast=ocean
r.mapcalc plume_try2=0

for i in `cat plume_raster.list`; do 
echo "Processing ${i}..."
r.mapcalc plume_temp = "plume_try2 + if( isnull(${i}), 0, ${i} )" 
g.remove rast=plume_try2 > /dev/null 2>&1
g.rename rast=plume_temp,plume_try2 > /dev/null 2>&1
done
