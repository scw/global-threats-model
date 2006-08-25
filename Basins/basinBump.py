# basinBump.py
# Rebuilds an elevation model with breaks (increase elevation), burns (decrease elevation)
# and drains (assigned nodata locations).  These forcings allow an accurate hydrological
# deliniation for the elevation surface.
#
# Author: scw <walbridge@nceas.ucsb.edu>
# Date: 3.27.2006
# Usage: basinBump <elevation> <breaks_shp> <burns_shp> <drains_shp> <output dir> <output prefix> 

# Import system modules
import sys, string, os, win32com.client

# Geoprocessor configuration
gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1") # Create the geoprocessor object
gp.CheckOutExtension("spatial")                                 # Check out the required license
gp.overwriteoutput = 1                                          # Overwrite existing files

if len(sys.argv) < 6:
	print "Usage: basinBump <elevation> <breaks_shp> <burns_shp> <drains_shp> <output dir> <output prefix>"
	sys.exit()

outputDir  = sys.argv[5]
outputName = sys.argv[6]
outputBase = outputDir + '\\' + outputName

inElem = { 'DEM'   : sys.argv[1], 'breaks' : sys.argv[2], \
           'burns' : sys.argv[3], 'drains' : sys.argv[4]}

for elemName, elemPath in inElem.items():
    (path, filename) = os.path.split(elemPath)
    if path == '':
        inElem[elemName] = outputDir + "\\" + filename

# Extent and cellsize should match input DEM
gp.extent   = inElem['DEM']
gp.cellsize = inElem['DEM']

'''print outputBase
print inElem
sys.exit()
'''

# output data
break_0 = outputBase + '_bk0'
burn_0  = outputBase + '_bn0'
drain_0 = outputBase + '_dn0'
drain_1 = outputBase + '_dn1'
drain_2 = outputBase + '_dn2'
drain_3 = outputBase + '_dn3'
combine = outputBase + '_dem'

try:
    print "F to R"
    # Process: Feature to Raster...
    gp.FeatureToRaster_conversion(inElem['breaks'], "Id", break_0, gp.cellsize)

    print "F to R2"
    # Process: Feature to Raster (2)...
    gp.FeatureToRaster_conversion(inElem['burns'], "Id", burn_0, gp.cellsize)

    print "F to R3"
    # Process: Feature to Raster (3)...
    gp.FeatureToRaster_conversion(inElem['drains'], "Id", drain_0, gp.cellsize)

    # Process: Is Null...
    gp.IsNull_sa(drain_0, drain_1)

    # Process: Con...
    gp.Con_sa(drain_1, '0', drain_2, '1', "")

    # Process: Set Null...
    gp.SetNull_sa(drain_2, '0', drain_3, "")

    print "At Map Algebra."
    # Process: Single Output Map Algebra...
    gp.SingleOutputMapAlgebra_sa("con(isnull(%s), 0, 200) + con(isnull(%s), 0, -400) + %s + %s" % (break_0, burn_0, drain_3, inElem['DEM']), combine)

    # Process: Build Pyramids...
    gp.BuildPyramids_management(combine)

except:
    # report geoprocessing errors
    print gp.GetMessages()
