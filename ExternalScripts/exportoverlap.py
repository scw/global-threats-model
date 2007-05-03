import win32com.client, sys, os
from win32com.client import Dispatch
gp = Dispatch("esriGeoprocessing.GPDispatch.1") 

 
for x in range (130,154):
    outputname = "waus" + str(x) + ".shp"
    gp.featureclasstofeatureclass("F:\global_basins\threats\shipping\tnc_ports\MW\ports_1000km_buff.shp", "F:\global_basins\threats\shipping\tnc_ports\MW\batch", outputname, '"fid" = ' + str(x)) 
