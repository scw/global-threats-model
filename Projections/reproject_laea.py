# ---------------------------------------------------------------------------
# reproject_laea.py
# Shaun Walbridge, 5.22.2006 <walbridge@nceas.ucsb.edu>
# Usage: reproject_laea <input_layer> 
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, win32com.client

gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")                  # Create the Geoprocessor object
gp.Overwriteoutput = 1                                                           # Overwrite existing files
gp.CheckOutExtension("spatial")                                                  # Check out any necessary licenses

# Script arguments...
if len(sys.argv) == 1:
  print "Usage: reproject_laea <input_file>"
  sys.exit()

# assumes WGS84 input. Could improve checking.
def project_to_laea (inputFeature):
    inputDir,  inputFile      = os.path.split(inputFeature)
    inputBase, inputExtension = os.path.splitext(inputFile)
    gp.workspace = inputDir
    
    # Location information: shortname, projection name
    continents = { 'af' : ['africa',       922.856981],
                   'as' : ['asia',         779.4213321],
                   'au' : ['australia',    908.9955774],
                   'eu' : ['europe',       702.5651599],
                   'na' : ['northAmerica', 779.4213321],
                   'pa' : ['pacific',      908.9955774],
                   'sa' : ['southAmerica', 908.9955774],
                 }
 
    continentPath    = "F:\\dev\\wgs_globe\\continents-beta\\"
    ext = ''
    wgsProjection    = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984'," \
                       "SPHEROID['WGS_1984',6378137.0,298.257223563]]," \
                       "PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
    dsDesc = gp.Describe(inputFile)
    dsType = str(dsDesc.DataSetType)
    
    if dsType == 'FeatureClass':
        ext = '.shp'

    for contShort, contData in continents.iteritems():
        contName, cellsize = contData
        projectionPath = sys.path[0] + '\\' + contName + '.prj'

        # Process : Project
        baseName = inputDir + '\\' + inputBase + '_' + contShort
        laeaName = contShort + '_' + inputBase[:5] + '_laea' + ext
        clipName = contShort + '_' + inputBase[:6] + ext
        contName = continentPath + contName + '.shp'

        #print 'laeaName: %s, basename: %s, clipName: %s, inputBase: %s' % (laeaName, baseName, clipName, inputBase)
               
        try:
            if dsType == 'FeatureClass':
                gp.project_management(inputFile, laeaName, projectionPath, "")
                gp.repairgeometry(laeaName)
                gp.clip_analysis(laeaName, contName, clipName, "")
            else:
                #print "projecting %s..." % laeaName
                print "gp.projectRaster(%s, %s, %s, 'NEAREST', %s)" % \
                (inputFeature, laeaName, projectionPath,cellsize)
                gp.projectRaster(inputFeature, laeaName, projectionPath, 'BILINEAR', cellsize)
                print "extracting by mask..."
                #gp.ExtractByMask_sa(laeaName, contName, clipName)
        except:
            print "error: " + gp.GetMessages()
    
project_to_laea(sys.argv[1])
