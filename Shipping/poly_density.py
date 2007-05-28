#!/usr/bin/env python
"""
 poly_density.py
 Calculate density of polygon data as a raster surface.
 Each raster cell contains a value indicating the percent cover of the underlying polygon.
 
 To get decent performance, it is absolutely essential that the input vector dataset have a gdal-recognized spatial index (ie a .qix file for shapefiles as created by shtree)

 Author: Matthew T. Perry

 License: You are free to use or modify this code for any purpose. Any derivative copy must clearly give credit to the original author. This license grants no warranty of any kind, express or implied. 
"""
import ogr
import sys
import os
import Numeric
import gdal

def getOpts():
    poly_ds = sys.argv[1] 
    filename = os.path.basename(os.path.splitext(poly_ds)[0])
    #poly_ds = "output/extract_clipped/bbox_n178_45.shp"
    poly_lyr = 0
    #extent = [-180., 40., -175., 50.]
    cellsize = 0.00833333333333
    outfile = "shipping_density_%s.tif" % filename
    format = "GTiff"
    return (poly_ds,poly_lyr,cellsize,outfile,format)    
   
if __name__ == "__main__":
    # Get the inputs
    (poly_ds,poly_lyr,cellsize,outfile,format) = getOpts()    

    # Get the input layer
    ds = ogr.Open(poly_ds)
    lyr = ds.GetLayer(poly_lyr)
    
    extent = lyr.GetExtent()
    # Confirm dataset is polygon and extents overlap 
    ydist = extent[3] - extent[2]
    xdist = extent[1] - extent[0]
    
    xcount = int((xdist/cellsize)+1)
    ycount = int((ydist/cellsize)+1)

    print xcount, ycount 

    # Create output raster  
    driver = gdal.GetDriverByName( format )
    dst_ds = driver.Create( outfile, xcount, ycount, 1, gdal.GDT_UInt16 )

    # the GT(2) and GT(4) coefficients are zero,     
    # and the GT(1) is pixel width, and GT(5) is pixel height.     
    # The (GT(0),GT(3)) position is the top left corner of the top left pixel
    gt = (extent[0],cellsize,0,extent[3],0,(cellsize*-1.))
    dst_ds.SetGeoTransform(gt)
    
    dst_band = dst_ds.GetRasterBand(1)
    dst_band.SetNoDataValue( -9999 )

    pixelnum = 0
    
    for ypos in range(ycount):
	    # Create output line array
        outArray = Numeric.zeros( (1, xcount) )
        maxy = extent[3] - ypos * cellsize
        miny = maxy - cellsize
        for xpos in range(xcount):
            # create a 4-item list of extents 
            minx = xpos * cellsize + extent[0] 
            maxx = minx + cellsize

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
            Numeric.put( outArray, xpos, feat_count )
            
            pixelnum += 1
 
        dst_band.WriteArray(outArray,0,ypos)
        pct_complete = (float(pixelnum)/(xcount*ycount) * 100.)
        #if pct_complete >= 10:
        #    sys.exit()

        print '%.2f pct complete' % pct_complete

    dst_ds = None
