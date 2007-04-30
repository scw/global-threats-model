
"""
plume_add_arc.py
ArcGIS Model to add batches of plumes together using Map Algebra

Authors: Shaun C. Walbridge
"""

# Import system modules
import sys, string, os, arcgisscripting, glob

# Create the Geoprocessor object
gp = arcgisscripting.create()

# Set the Geoprocessing environment...
gp.outputCoordinateSystem = "PROJCS['World_Mollweide',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mollweide'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]"
gp.extent = "-17703215.5609692 -9018645.62975446 17876133.2023738 \
8750470.21662275" # pulled from GRASS ocean layer

# EDIT ME: change to the directory containing the compressed GeoTiffs
ws = "F:\\dev\\p3_fert"

if not os.path.isdir(ws):
    ws = os.getcwd()

gp.workspace = ws
gp.CheckOutExtension("Spatial")
name = os.path.basename(ws)

# EDIT ME: pattern below matches the files you'd like to add
files = glob.glob('plume*.tif*')
r = 'zyxwvutsrqponmlkjihgfedcba'
ra  = [r[i] for i in range(len(r))]
pass2 = pass3 = []

try:
    for i in range(0, len(files), 10): # add 10 rasters per run
        exp = " + ".join(files[i:i + 9])
        output ='%s_%s.tif' % (name, ra.pop())
        pass2.append(output)
        print "generating %s" % output
        gp.SingleOutputMapAlgebra("(%s)" % exp, output)
   
    
    for i in range(0, len(pass2), 5): # add 5 rasters per run
        exp = " + ".join(pass2[i:i+4])
        output = '%s_%s_2.tif' % (name, ra.pop())
        pass3.append(output)
        print "generating %s" % output
        gp.SingleOutputMapAlgebra("(%s)" % exp, output)
    
    exp = " + ".join(pass3)
    print "generating merged final output %s." % name
    gp.SingleOutputMapAlgebra("(%s)" % exp, '%s.tif' % name)

except:
    print gp.GetMessages()
