print"---------------------------------------------------------------"
print"mxdexporter.py"
print " by G.B.Gabrisch     gerry@gabrisch.us"
print "----------------------------------------------------------------"

# Import system modules
import sys, string, os, shutil, win32com.client

# Create the Geoprocessor object
gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")

# Load required toolboxes...
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")


print "Step 1: Before using this script you must install"
print "and run the WriteFilePaths2Text.bas file in ArcMap."
print "If you have not done so, quit now and view the readme file that accompanied this script."
print 
print
print "Step 2: Create a new folder, save your mxd to that folder, run the WriteFilePaths2Text tool."
print


#map to the folder
Output_Folder = raw_input("Enter the path to the output folder, press <enter>:  ")
print
#map to the mxd
TheMXD = raw_input("Enter the name of the mxd, DO NOT ENTER THE FILE EXTENSION, press <enter>")
print

b=0

MyText = Output_Folder+"\\"+TheMXD+".txt"

print "Reading file: "+MyText
f = open(MyText,'r')
lines=f.readlines()
f.close()
a=len(lines)

print "Please stand by..."

x=1
y=0
z=2
q=3
try:
	while b<a:
		s= lines[x]
		s=str(s)
		print s
		s=s.rstrip()
		w= "Shapefile Feature Class"
		r= "Raster Dataset"
		pgfc ="Personal Geodatabase Feature Class"

		if s == pgfc:
			print "working on Personal Geodatabase Feature Class..."
			thegeodatabase= lines[z]
			thegeodatabase=str(thegeodatabase)
			thegeodatabase=thegeodatabase.rstrip()
			
			thegeodatabasename=thegeodatabase.split("\\")
			
			thegeodatabasename=thegeodatabasename.pop()
			thegeodatabasename=thegeodatabasename.lstrip()
		
			print thegeodatabasename
			OutputFeature=Output_Folder+thegeodatabasename
			print OutputFeature
			# Process: Copy...
			gp.Copy_management(thegeodatabase, OutputFeature, "Workspace")

			print "Geodatabase Export Finished"


#process a shapefile
		elif s == w:
			pathtofile= lines[z]
			pathtofile=str(pathtofile)
			pathtofile=pathtofile.rstrip()
			layername=lines[y]
			layername=str(layername)
			layername=layername.rstrip()
			print pathtofile
			print layername
			pathnameandextension= pathtofile+ ".shp"
			print pathnameandextension
			OutputFeature=Output_Folder+"\\"+layername+".shp"
			print OutputFeature
			gp.CopyFeatures_management(pathnameandextension, OutputFeature, "", "0", "0", "0")
			print "Shapefile Export Finished"



#process raster		
		elif s == r:

			pathtofile= lines[q]
			pathtofile=str(pathtofile)
			pathtofile=pathtofile.rstrip()
			layername=lines[y]
			layername=str(layername)
			layername=layername.rstrip()
			extension=lines[y]
			extension=str(extension)
			extension=extension.rstrip()
			extension=extension.split(".")
			extension=extension.pop()
			extension=extension.lstrip()
			pathtofile2= pathtofile+ layername
			OutputFeature=Output_Folder + "\\" + layername
			
			if extension=="jpg" or "JPG":
				print "jpg encountered"
				print "copy to "+ OutputFeature
				shutil.copy(pathtofile2,OutputFeature)


				
				
				nameonly=layername
				print "nameonly =" +nameonly
				nameonly=nameonly.lstrip()
				nameonly=nameonly.split(".")
				nameonly=nameonly[0]
				print "striped name only= " + nameonly

				nameonly=nameonly + ".jgw"
				print "concantoned nameonly =" +nameonly
				pathtofile3=pathtofile + nameonly
				print "pathtofile3 "+ pathtofile3
				OutputFeature2 = Output_Folder + nameonly
				print OutputFeature2
				shutil.copy(pathtofile3,OutputFeature2)


			
			else:
				print "path to file ="+ pathtofile
				print "OutputFeature= " + OutputFeature
				gp.CopyRaster_management(pathtofile, OutputFeature, "", "", "", "NONE", "NONE", "")
				print "Raster Export Finished"
		else:
			print s+" This mxd contains an unsupported file type."
			b=b+4	

			
		x=x+4
		y=y+4
		z=z+4
		q=q+4

except:
    gp.AddMessage(gp.GetMessages(2))
    print gp.GetMessages(2)

#Ends the script        

stopme = raw_input ("your script has finished, press enter to end")