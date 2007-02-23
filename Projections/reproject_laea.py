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

    # Location information: shortname, projection name, central meridian, latitude of origin
    continents = { 'af' : [ 'africa',        '20.0',  '5.0', 922.856981], 
                   'as' : [ 'asia',         '100.0', '45.0', 779.4213321], 
                   'au' : [ 'australia',    '135.0','-15.0', 908.9955774], 
                   'eu' : [ 'europe',        '20.0', '55.0', 702.5651599], 
                   'na' : [ 'northAmerica','-100.0', '45.0', 779.4213321], 
                   'pa' : [ 'pacific',     '-170.0','-15.0', 908.9955774], 
                   'sa' : [ 'southAmerica', '-60.0','-15.0', 908.9955774] }

    continentPath    = "F:\\dev\\wgs_globe\\continents-beta\\"
    meridian         = latitude = ext = ''
    wgsProjection    = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984'," \
                       "SPHEROID['WGS_1984',6378137.0,298.257223563]]," \
                       "PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
    dsDesc = gp.Describe(inputFile)
    dsType = str(dsDesc.DataSetType)
    
    if dsType == 'FeatureClass':
        ext = '.shp'

    for contShort, contList in continents.iteritems():
        contName, meridian, latitude, cellsize = contList
        projectionString = "PROJCS['Lambert_Azimuthal_Equal_Area'," \
                           "GEOGCS['GCS_WGS_1984'," \
                             "DATUM['D_WGS_1984'," \
                             "SPHEROID['WGS_1984',6378137.0,298.257223563]]," \
                             "PRIMEM['Greenwich',0.0]," \
                             "UNIT['Degree',0.0174532925199433]]," \
                           "PROJECTION['Lambert_Azimuthal_Equal_Area']," \
                           "PARAMETER['False_Easting',0.0]," \
                           "PARAMETER['False_Northing',0.0]," \
                           "PARAMETER['Central_Meridian',"   + meridian + "]," \
                           "PARAMETER['Latitude_Of_Origin'," + latitude + "]," \
                           "UNIT['Meter',1.0]]"

        # Process : Project
        baseName = inputDir + '\\' + inputBase + '_' + contShort
        laeaName = contShort + '_' + inputBase[:6] + '_lae' + ext
        clipName = contShort + '_' + inputBase[:6] + ext
        contName = continentPath + contName + '.shp'
        dsDesc2 = gp.Describe(inputFile)
        dsType2 = str(dsDesc.DataSetType)
        #print 'laeaName: %s, basename: %s, clipName: %s, inputBase: %s' % (laeaName, baseName, clipName, inputBase)
        #print "gp.projectRaster(%s, %s, %s, \"BILINEAR\", %s)" % (input, laeaName, projectionString, cellsize)
        
        try:
            if dsType == 'FeatureClass':
                gp.project_management(inputFile, laeaName, projectionString, "")
                gp.repairgeometry(laeaName)
                gp.clip_analysis(laeaName, contName, clipName, "")
            else:
                
                print "projecting %s..." % laeaName
                gp.projectRaster(inputFile, laeaName, projectionString, "NEAREST", cellsize)
                print "extracting by mask..."
                gp.ExtractByMask_sa(laeaName, contName, clipName)
        except:
            print "error: " + gp.GetMessages()
    
project_to_laea(sys.argv[1])
