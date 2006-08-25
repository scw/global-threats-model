# basinBuild.py
# Author scw <walbridge@nceas.ucsb.edu>
# Date: 3.10.2006
# Usage: buildbasin ulx uly llx lly directory file_prefix

# Import system modules
import sys, string, os, win32com.client
from urllib import urlretrieve

# Create the Geoprocessor object
gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1") # Create the geoprocessor object 	 
gp.CheckOutExtension("spatial")                                 # Check out the required license
gp.overwriteoutput = 1                                          # Overwrite existing files

# Load required toolboxes...
#gp.AddToolbox("Data Management Tools.tbx")
#gp.AddToolbox("Spatial Analyst Tools.tbx")
#gp.AddToolbox("Conversion Tools.tbx")

# WCS URL for downloading SRTM90 tiles
wcsUrl = 'http://cabrillo.nceas.ucsb.edu:8080/cgi-bin/mapserv?map=/opt/geodev/mapserver/srtm.map' \
         '&Version=1.0.0&request=GetCoverage&Coverage=srtm&service=WCS&CRS=EPSG:4326&Format='     \
         'image/geotiffint16&resx=0.0008333333&resy=0.0008333333&BBOX='

# input coordinates: inputUlx inputUly inputLlx inputLly, ex: -124 40 -122 42
# domain checking. OGC WCS spec uses BBOX of {minx, miny, maxx, maxy}.
domain = {'x' : [float(sys.argv[1]), float(sys.argv[3])], 
          'y' : [float(sys.argv[2]), float(sys.argv[4])]}

bBox = [min(domain['x']), min(domain['y']), max(domain['x']), max(domain['y'])]

# convert the floats back into a string, perform list comprehension
urlBbox = ','.join(["%.6f" % k for k in bBox])
urlFull = wcsUrl + urlBbox

#print urlFull
outputDir = sys.argv[5]
if outputDir == '#':
  outputDir = "F:\\dev\\srtm_hydro\\b\\"

outputName = sys.argv[6]
if outputName == '#':
  outputName = 'test'

outputBase = outputDir + outputName
outputFile = outputBase + '.tif'
print "downloading SRTM 90m (%s):"% urlBbox,
urlReturn  = urlretrieve(urlFull, outputFile)
print "\tcomplete."

basinFlowdir   = outputBase + '_fdir'
basinFlowacc   = outputBase + '_facc'
basinFtmp      = outputBase + '_ftmp'
basinFill      = outputBase + '_fill'
basinRaster    = outputBase 
basinShapefile = outputBase + '_basin.shp'

try:
  # incoming GeoTiffs have no proper nulls, set these
  print "removing null values:",
  gp.SetNull_sa(outputFile, outputFile, basinFtmp, "VALUE = -32768")
  print "\t\t\t\t\tcomplete."

  # process the DEM with a fill operation, default depth 100m
  print "filling dem sinks:"
  gp.Fill_sa(basinFtmp, basinFill, "25")
  print "\t\t\t\t\t\t\tcomplete."
  
  # Process: Flow Direction...
  print "computing flowdirection:",
  gp.FlowDirection_sa(basinFill, basinFlowdir, "NORMAL", '#')
  print "\t\t\t\tcomplete."
  
  # Process: Flow Accumulation...
  print "computing flowaccumulation:",
  gp.FlowAccumulation_sa(basinFlowdir, basinFlowacc, "")
  print "\t\t\t\tcomplete."
  
  # Process: Batch Build Pyramids...
  print "generating image overviews:",
  gp.BatchBuildPyramids_management(basinFlowdir+';'+basinFlowacc+';'+basinFill)
  print "\t\t\t\tcomplete."
  
  # Process: Basin...
  print "computing basins:",
  gp.Basin_sa(basinFlowdir, basinRaster)
  print "\t\t\t\t\tcomplete."

  # Process: Raster to Polygon...
  print "vectorizing basins:",
  gp.RasterToPolygon_conversion(basinRaster, basinShapefile, "NO_SIMPLIFY", "VALUE")
  print "\t\t\t\t\tcomplete."
  print "output basins: %s" %basinShapefile

except:
    # report geoprocessing errors
    print gp.GetMessages()
