# basinBump.py
# Rebuilds an elevation model with breaks (increase elevation), burns (decrease elevation)
# and drains (assign nodata locations).  These forcings allow an accurate hydrological
# deliniation for the elevation surface. Also allows changes in the 
#
# Author: scw <walbridge@nceas.ucsb.edu>
# Date: 3.27.2006
# Usage: basinBump <prefix> <elevation> <modifications dir> <output dir>
# 
# Usage Example: The DEM is named "eu_ult_clip" and the modifications folder is "modifications".
#                You want to output the results to the "build_try1" folder:
#                basinBump.py eu c:\dev\eu\eu_ult_clip c:\dev\eu\mods c:\dev\eu\build_try1

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

if len(sys.argv) < 4:
	print "Usage: basinBump <prefix> <elevation> <modifications dir> <output dir>"
	sys.exit()

try:
    
    prefix = sys.argv[1]
    demarg = sys.argv[2]
    modDir = sys.argv[3]
    outputDir  = sys.argv[4]
    
except:
    ########## EDIT THESE IF YOU'RE LAZY AND DONT WANT TO TYPE CL PARAMS #######
    prefix = "as_se"	
    outputDir  = "F:\\dev\wgs_globe\\asia\\as_dev2\\tmp"
    demarg = "F:\\dev\wgs_globe\\asia\\as_dev2\\tmp"
    modDir = ""
    ###########

# clean up directories
paths = {'mod' : modDir, 'out' : outputDir}
for name, path in paths.items():
    if path.endswith('\\'):
        paths[name] = paths[name][:-1]
    paths[name] += "\\" + prefix

modElem = ['breaks', 'burns', 'fill', 'fill_area', 'null', 'null_area']
inElem = { 'DEM'   : demarg, }

for mod in modElem:
    inElem[mod] = "%s_%s.shp" % (paths['mod'], mod)
    
# Extent and cellsize should match input DEM
gp.extent   = inElem['DEM']
gp.cellsize = inElem['DEM']

# debug:
# print inElem

# output data
infill_0 = paths['out'] + '_if0'
infill_1 = paths['out'] + '_if1'
infill_2 = paths['out'] + '_if2'
fill_0 = paths['out'] + '_fi0'
fill_1 = paths['out'] + '_fi1'
fill_2 = paths['out'] + '_fi2'
innulls_0 = paths['out'] + '_in0'
innulls_1 = paths['out'] + '_in1'
innulls_2 = paths['out'] + '_in2'
innulls_3 = paths['out'] + '_in3'
nulls_0 = paths['out'] + '_nf0'
nulls_1 = paths['out'] + '_nf1'
nulls_2 = paths['out'] + '_nf2'
nulls_3 = paths['out'] + '_nf3'
break_0 = paths['out'] + '_bk0'
burn_0  = paths['out'] + '_bn0'
combine = paths['out'] + '_dem'

try:
    print "Rasterizing fill-in (area)"
    gp.FeatureToRaster_conversion(inElem['fill_area'], 1000, infill_0, gp.cellsize)
    gp.Plus_sa(infill_0, 1000, infill_1)
    gp.SingleOutputMapAlgebra_sa("con( isnull( %s ), %s, %s)" % \
                                 (inElem['DEM'], infill_1, inElem['DEM']), infill_2)

    print "Rasterizing fills (point)"
    gp.FeatureToRaster_conversion(inElem['fill'], 1000, fill_0, gp.cellsize)
    gp.Plus_sa(fill_0, 1000, fill_1)
    gp.SingleOutputMapAlgebra_sa("con( isnull( %s ), %s, %s)" % \
                                (infill_2, fill_1, infill_2), fill_2)
    
    print "Rasterizing nulls (area)"
    gp.FeatureToRaster_conversion(inElem['null_area'], 0, innulls_0, gp.cellsize)

    gp.IsNull_sa(innulls_0, innulls_1)
    gp.Con_sa(innulls_1, '0', innulls_2, '1', "")
    gp.SetNull_sa(innulls_2, '0', innulls_3, "")
                                     
    print "Raserizing nulls (point)"
    gp.FeatureToRaster_conversion(inElem['null'], 0, nulls_0, gp.cellsize)
  
    gp.IsNull_sa(nulls_0, nulls_1)
    gp.Con_sa(nulls_1, '0', nulls_2, '1', "")
    gp.SetNull_sa(nulls_2, '0', nulls_3, "")
                                  
    print "Rasterizing breaks"
    # Process: Feature to Raster...
    gp.FeatureToRaster_conversion(inElem['breaks'], "Id", break_0, gp.cellsize)
    
    print "Rasterizing burns"
    # Process: Feature to Raster (2)...
    gp.FeatureToRaster_conversion(inElem['burns'], "Id", burn_0, gp.cellsize)
 
    print "Combining layers into one modified DEM"
    # Process: Single Output Map Algebra...
    gp.SingleOutputMapAlgebra_sa("con(isnull(%s), 0, 200) + con(isnull(%s), 0, -400) + %s + %s + %s" %  \
                                 (break_0, burn_0, nulls_3, innulls_3, fill_2), combine)

    print "Building Pyrimids"
    # Process: Build Pyramids...
    gp.BuildPyramids_management(combine)

except:
    # report geoprocessing errors
    print gp.GetMessages()
