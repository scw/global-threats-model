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

# Load required toolboxes...
#gp.AddToolbox("F:/gis/a9/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")
#gp.AddToolbox("F:/gis/a9/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")
#gp.AddToolbox("F:/gis/a9/ArcGIS/ArcToolbox/Toolboxes/Conversion Tools.tbx")

#if len(sys.argv) < 6:
#	print "Usage: basinBump <elevation> <infill_shp> <breaks_shp> <burns_shp> <drains_shp> <output dir> <output prefix>"
#	sys.exit()

try:	
    demarg = sys.argv[1]
    infillarg = sys.argv[2]
    breaksarg = sys.argv[3]
    burnsarg = sys.argv[4]
    drainsarg = sys.argv[5]
    outputDir  = sys.argv[6]
    outputName = sys.argv[7]
except:
    ########## EDIT THESE IF YOU'RE LAZY AND DONT WANT TO TYPE CL PARAMS #######
    outputName = "af"	
    outputDir  = "C:\\WorkSpace\\srtm_basins\\af_basins\\build_try4"
    ### and to a lesser extent, these
    demarg = "C:\\WorkSpace\\srtm_basins\\af_basins\\af_ult_fix2"
    infillarg = "C:\\WorkSpace\\srtm_basins\\af_basins\\af_fills.shp"
    breaksarg = "C:\\WorkSpace\\srtm_basins\\af_basins\\af_breaks.shp"
    burnsarg = "C:\\WorkSpace\\srtm_basins\\af_basins\\af_burns.shp"
    drainsarg = "C:\\WorkSpace\\srtm_basins\\af_basins\\af_drains.shp"
    ###########


outputBase = outputDir + "\\" + outputName

inElem = { 'DEM'   : demarg, 'breaks' : breaksarg, \
           'burns' : burnsarg, 'drains' : drainsarg, 'infill': infillarg}

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
infill_0 = outputBase + '_if0'
infill_1 = outputBase + '_if1'
break_0 = outputBase + '_bk0'
burn_0  = outputBase + '_bn0'
drain_0 = outputBase + '_dn0'
drain_1 = outputBase + '_dn1'
drain_2 = outputBase + '_dn2'
drain_3 = outputBase + '_dn3'
combine = outputBase + '_dem'

try:
    print "Infilling the DEM"
    # Process: Feature to Raster...
    gp.FeatureToRaster_conversion(inElem['infill'], "Id", infill_0, gp.cellsize)
    gp.SingleOutputMapAlgebra_sa("con( isnull( %s ), %s, %s )" \
                                 % (inElem['DEM'], infill_0, inElem['DEM']), infill_1)

    print "Rasterizing breaks"
    # Process: Feature to Raster...
    gp.FeatureToRaster_conversion(inElem['breaks'], "Id", break_0, gp.cellsize)
    
    print "Rasterizing burns"
    # Process: Feature to Raster (2)...
    gp.FeatureToRaster_conversion(inElem['burns'], "Id", burn_0, gp.cellsize)

    print "Rasterizing drains"
    # Process: Feature to Raster (3)...
    gp.FeatureToRaster_conversion(inElem['drains'], "Id", drain_0, gp.cellsize)

    # Process: Is Null...
    gp.IsNull_sa(drain_0, drain_1)

    # Process: Con...
    gp.Con_sa(drain_1, '0', drain_2, '1', "")

    # Process: Set Null...
    gp.SetNull_sa(drain_2, '0', drain_3, "")

    print "Combining layers into one modified DEM"
    # Process: Single Output Map Algebra...
    gp.SingleOutputMapAlgebra_sa("con(isnull(%s), 0, 200) + con(isnull(%s), 0, -400) + %s + %s" % (break_0, burn_0, drain_3, infill_1), combine)

    print "Building Pyrimids"
    # Process: Build Pyramids...
    gp.BuildPyramids_management(combine)

except:
    # report geoprocessing errors
    print gp.GetMessages()
