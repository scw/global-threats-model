# terra_stats.py
# calculate per-basin statistics
# Author: scw <walbridge@nceas.ucsb.edu>
# Date: 3.20.2007
# Usage: terra_stats.py

# Import system modules
import sys, string, os

# Create the geoprocessor object
try:
    import arcgisscripting
    gp = arcgisscripting.create()

except:
    import win32com.client
    gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1") 

# Geoprocessor configuration
gp.CheckOutExtension("spatial")                                 # Check out the required license
gp.overwriteoutput = 1                                          # Overwrite existing files

"""
if len(sys.argv) < 4:
	print "Usage: basinBump <prefix> <elevation> <modifications dir> <output dir>"
	sys.exit()
"""
try:
  
    prefix = sys.argv[1]
    demarg = sys.argv[2]
    modDir = sys.argv[3]
    outputDir  = sys.argv[4]
    
except:
    prefixes   = ['af', 'as', 'au', 'eu', 'na', 'pa', 'sa']	
    outpath    = "X:\\data\\marine_threats\\work\\raster_stats\\outputs"
    rasters    = ['fertc', 'pestc']
    rasterbase = "F:\\dev"
    basins     = "F:\\dev\\basins"

try:
    for r in rasters:
        gp.workspace = "%s\\%s" % (rasterbase, r)
        for p in prefixes:
            zones = "%s\\%s_bas_orig.shp" % (basins, p)
            rast = "%s_%s" % (p, r)
            table = "%s\\%s\\%s_zonal_stats_%s.dbf" % (outpath, p, p, r)
            gp.ZonalStatisticsAsTable_sa(zones, "basin_id", rast, table, "DATA")

except:
    # report geoprocessing errors
    print gp.GetMessages()
