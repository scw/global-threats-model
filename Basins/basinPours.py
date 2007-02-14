# basinPours.py
# finds the pour points for an input basin model and flow accumulation.
#
# Author: scw <walbridge@nceas.ucsb.edu>
# Date: 3.28.2006
# Usage: basinPours <basin_shp> <flow accumulation> <output dir> <output prefix> 


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

if len(sys.argv) < 5:
	print "Usage: basinPours <basin_shp> <flow accumulation> <output dir> <output prefix>"
	sys.exit()

outputDir  = sys.argv[3]
outputName = sys.argv[4]
outputBase = outputDir + '\\' + outputName

inElem = { 'basins'   : sys.argv[1], 'facc' : sys.argv[2]}

for elemName, elemPath in inElem.items():
    (path, filename) = os.path.split(elemPath)
    if path == '':
        inElem[elemName] = outputDir + "\\" + filename

# Extent and cellsize should match input flow accumulation
gp.extent   = inElem['facc']
gp.cellsize = inElem['facc']

# output data
basins       = outputBase + '_bas'
basins_zmax  = outputBase + '_zmax'
basins_zmax2 = outputBase + '_zmax2'
outlets      = outputBase + '_outlet'
basins_int   = outputBase + '_int'
outlets_shp  = outputBase + '_processed.shp'

try:
    # convert input basins feature layer into a raster file matching extent of facc
    gp.FeatureToRaster_conversion(inElem['basins'], "ID", basins, gp.cellsize)

    # Process: Zonal Statistics...
    gp.ZonalStatistics_sa(basins, "Value", inElem['facc'], basins_zmax, "MAXIMUM", "DATA")

    # Process: Single Output Map Algebra...
    gp.SingleOutputMapAlgebra_sa("con(%s == %s, %s, -99)" % (basins_zmax, inElem['facc'], inElem['facc']), basins_zmax2)

    # Process: Single Output Map Algebra (2)...
    gp.SingleOutputMapAlgebra_sa("setnull(%s == -99, %s)" % (basins_zmax2, basins_zmax2), outlets)

    # Process: Int...
    gp.Int_sa(outlets, basins_int)

    # Process: Raster to Point...
    gp.RasterToPoint_conversion(basins_int, outlets_shp, "VALUE")

except:
    # report geoprocessing errors
    print gp.GetMessages()
