# cru_combine.py
# Description: Add together a large number of rasters, summarizing values
# Author: scw, walbridge@nceas.ucsb.edu
# Date: 6.24.2005
# Import COM Dispatch module

from win32com.client import Dispatch 	 

GP = Dispatch("esriGeoprocessing.GPDispatch.1") # Create the geoprocessor object 	 
GP.CheckOutExtension("Spatial")                 # Check out the required license
GP.overwriteoutput = 1                          # Overwrite existing files
ws = 'f:/dev/cru_precip/'                       # Set the workspace


decades = ['196', '197', '198', '199', '200']
GP.Workspace = ws
count = 0
rlist = ''

try:
    for dec in decades:
        fcs = GP.ListRasters('prn_' + dec + '*') 	 
        fcs.reset()
        fc = fcs.next() 	 
        inputs = ws + fc 	 
        # Get the next name and start the loop 	 
        fc = fcs.next()
        count = count + 1
        
        while fc: # While the fc name is not empty
            inputs = inputs + ";" + ws + fc	 
            fc = fcs.next()
            count = count + 1
            
        outRaster = "f:/dev/cru_tmp/c_" + dec + '0s'
        rlist = rlist + ";" + outRaster
        
        # Process: Cell Statistics...
        GP.CellStatistics_sa(inList, outRaster, "SUM")
        print 'Combined the ' + dec + '0s elements into: ' + outRaster + ' Count: %i' % count
    
    # take decadal products and generate 50 year sum
    rlist = rlist[1:]
    outRaster = "f:/dev/cru_tmp/c_all"
    GP.CellStatistics_sa(rlist, outRaster, "SUM")
      
    print 'Combined the %i elements into ' % count + outRaster
    
    # divide the summed grid by the grid count to obtain an average
    outAverage = "f:/dev/cru_tmp/c_avg"
    GP.Divide_sa(outRaster, count, outAverage)

    print 'Sum / count calculated into ' + outAverage

    # set the dummy values to NULL
    outComplete = "f:/dev/cru_tmp/c_full"
    GP.SetNull_sa(outAverage, outAverage, outComplete, "VALUE < 0")
    print 'Set NULL Values into ' + outComplete

except:
    GP.GetMessages()
    