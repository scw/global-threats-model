# CellStatistics_sample.py
# Description: Calculates a per-cell statistic from multiple rasters
# Requirements: None
# Author: ESRI
# Date: 12/01/03

# Import system modules
import sys, string, os, win32com.client

# Create the Geoprocessor object
gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")

try:
    # Set local variables
    outRaster = "F:/dev/cru_tmp/comb_3"

    # Check out Spatial Analyst extension license
    gp.CheckOutExtension("Spatial")
    GP.Workspace= "f:/dev/cru_2/"
   
    # Process: Cell Statistics...
    gp.CellStatistics_sa("'f:/dev/cru_2/prn_2000_apr';'f:/dev/cru_2/prn_2000_jun'", outRaster, "MEAN")

except:
    # Print error message if an error occurs
    gp.GetMessages()

