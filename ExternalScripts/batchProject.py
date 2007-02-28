# ---------------------------------------------------------------------------
# batchproject.py

# Created By: Matthew Stayner
# E-mail : mstayner@bowencollins.com
# ---------------------------------------------------------------------------

#Purpose:
#  To batch project Raster data. Tested for TIFF, GRIDS, JPEG ETC.
#  

#Requirement
#  Attach this script to a tool in ArcToolbox.
#  Developed in ArcGIS ArcView licence Version 9.1
#  You May have to change the Toolbox path from D:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management  
#  Tools.tbx
#  to    C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx  or vice-versa

#Properties (right-click on the tool )
#General
#  Name        BatchRasterProject
#  Label       Batch Raster Project
#  Description   Projects all raster images in a user-specified folder to a user-defined coordinate system.
#                The new projected file has the same name as the original file and resides in the new user-specified folder. 
#
#Source script batchproject.py
#
#Parameter list
#                                      Parameter Properties
#           Display Name                    Data type              Type    Direction  MultiValue
#  argv[1]  Select the input folder          Folder               Required  Input      No
#  argv[2]  Select the output folder         Folder               Required  Input      No
#  argv[3]  Select the Coordinate System  Coordinate System       Required  Input      No





# Import system modules
import sys, string, os, win32com.client

# Create the Geoprocessor object
gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")

# Load required toolboxes...
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")

gp.workspace = sys.argv[1]
InFolder = sys.argv[1]
OutFolder = sys.argv[2]
coordinate = sys.argv[3]
try:
  RasterClassList = gp.ListRasters()
  RasterClassList.Reset()
  RasterImage = RasterClassList.Next()
  gp.AddMessage("\n" + "Begin Processing......." + "\n")
  while RasterImage:
    gp.AddMessage(" Projecting  " + RasterImage)
    InFileName = InFolder + "/" + RasterImage
    OutFileName = OutFolder + "/" + RasterImage
    gp.ProjectRaster_management(InFileName, OutFileName, coordinate)
    gp.AddMessage(RasterImage + "  Projected")
    gp.AddMessage("\n")
    RasterImage = RasterClassList.Next()
except:
  print gp.GetMessages(2)