# cru_combine.py
# Description: Add together a large number of rasters, summarizing values
# Author: scw, walbridge@nceas.ucsb.edu
# Date: 6.24.2005

# Import system modules
import sys, string, os, win32com.client

# Create the Geoprocessor object
gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")

# Set local variables
months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'nov', 'dec')
years = range(1961, 1962)
path = "F:/dev/cru_precip/"
precip = ''

try:
    for i in years:
        for j in months:
            precip += '\'%sprn_%i_%s\';' % (path, i, j)



    precip = precip[0:-1]
    
    #print 'precip: `%s`' % precip
    
    # Check out Spatial Analyst extension license
    gp.CheckOutExtension("Spatial")
    outRaster = "f:/dev/cru_tmp/61_test"
    
    # Process: Fill
    gp.CellStatistics_sa(precip, outRaster, "SUM")

except:
    # Print error message if an error occurs
    gp.GetMessages()

