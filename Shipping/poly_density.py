#!/usr/bin/env python
"""
 poly_density.py
 Calculate density of polygon data as a raster surface.
 Each raster cell contains a value indicating the percent cover of the underlying polygon.
 
 To get decent performance, it is absolutely essential that the input vector dataset have a gdal-recognized spatial index (ie a .qix file for shapefiles as created by shtree)

 Author: Matthew T. Perry, Shaun C. Walbridge

 License: You are free to use or modify this code for any purpose. Any derivative copy must clearly give credit to the original author. This license grants no warranty of any kind, express or implied. 
"""
import ogr
import sys
import os
import array

def getOpts():
    poly_ds = sys.argv[1] 
    filename = os.path.basename(os.path.splitext(poly_ds)[0])
    poly_lyr = 0
    cellsize = 0.008333333333333333
    outfile = "shipping_density_%s.asc" % filename
    return (poly_ds,poly_lyr,cellsize,outfile)    
   
if __name__ == "__main__":
    # Get the inputs
    (poly_ds,poly_lyr,cellsize,outfile) = getOpts()    

    # Get the input layer
    ds = ogr.Open(poly_ds)
    lyr = ds.GetLayer(poly_lyr)
   
    # GetExtent returns [minx, maxx, miny, maxy]
    extent = lyr.GetExtent()

    # ASCII file for writing data to
    asc = open(outfile, 'w')

    # Confirm dataset is polygon and extents overlap 
    ydist = extent[3] - extent[2]
    xdist = extent[1] - extent[0]
    
    xcount = int((xdist/cellsize)) # was +1
    ycount = int((ydist/cellsize)) # was +1

    print xcount, ycount 
    # write the ASCII Grid header
    asc.write("ncols %s\n" % xcount)
    asc.write("nrows %s\n" % ycount)
    asc.write("xllcorner %s\n" % extent[0])
    asc.write("yllcorner %s\n" % extent[2])
    asc.write("cellsize %s\n" % '0.008333333333333')
    asc.write("nodata_value %s\n" % -9999)

    # map integers to their string versions
    textlookup = dict([(i, ("%d" %i)) for i in range(-9999, 2**15)])
    
    pixelnum = 0
    
    for ypos in range(ycount):
	    # Create output line array
        outArray = array.array("h")
        for xpos in range(xcount):
            # create a 4-item list of extents 
            minx = xpos * cellsize + extent[0] 
            maxx = minx + cellsize
            maxy = extent[3] - ypos * cellsize
            miny = maxy - cellsize

            # Create Polygon geometry from BBOX
            wkt = 'POLYGON ((%f %f, %f %f, %f %f, %f %f, %f %f))' \
               % (minx, miny, minx, maxy, maxx, maxy, maxx, miny, minx, miny)
            g = ogr.CreateGeometryFromWkt(wkt)
            
            # Set spatial filter
            lyr.SetSpatialFilter(g)
            
            # Loop through all features/geometries w/in filter
            feat = lyr.GetNextFeature()
            feat_count = 0
            # this loop just kills performance...
            while feat is not None:
                # Check if polygon overlaps current cell
                sg = feat.GetGeometryRef().Distance(g)
                if sg < 0.0001:
                    feat_count += 1
                feat = lyr.GetNextFeature()
            
            lyr.ResetReading()

            #Assign total overlapping polys as value in line array
            outArray.append(feat_count) 
            pixelnum += 1
 
        textvalues = map(textlookup.__getitem__, outArray.tolist())
        asc.write(" ".join(textvalues))
        asc.write("\n")
        pct_complete = (float(pixelnum)/(xcount*ycount) * 100.)
        #if pct_complete >= 10:
        #    sys.exit()

        print '%.2f pct complete' % pct_complete
