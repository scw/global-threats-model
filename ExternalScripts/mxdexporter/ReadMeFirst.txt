The mxdexporter tool allows you to automate the copying of all the shapefiles, personal geodatabase feature classes, grids, tif, and jpg files in an mxd project to a new folder. 

This tool contains a VB scripted tool and a python script. The VB script codes a button in ArcMap, which when executed, will create a text file that stores the layer file paths and names used by the mxd.  Next, a python script reads the text file and creates copies of the layers into the same folder that contains the mxd document.  


Outline of Steps

	1. Install the WriteLayerPaths2txt.bas. (One time only)
	2. Install the WriteLayerPaths2txt button in ArcMap (One time only)
	3. Save your mxd (with relative paths) to a new empty folder.
	4. Execute the WriteLayerPath2txt tool.
	5. Run mxdexporter.py
	6. The mxdexporter.py is case sensitive, read below for other potential problems.

Procedure

Install the VB Code (One Time Only)

1. Install the WriteLayerPathsetxt.bas tool in ArcMap.
a. Start ArcMap-choose Tools-Macros-VBEditor.
b. In the Project-Normal Box, Highlight Normal (Normal.mxt)
c. Place the mouse curser on Normal (Normal.mxt), right mouse click and select Import File.
d. Navigate to the WriteLayerPaths2TXT.bas file and press the Open button>
e. Save
d. Close the VB editor.

Install the Tool (One Time Only)

1. ArcMap -> Tools dropdown menu -> Customize
2. Go to the "Commands" tab and select the "Macros" category.
3. Drag the new command onto an ArcMap Toolbar. It should be listed in the Commands Window as Nornal.WriteFilePaths2TXT.ListSources
4. Change the button's appearance if you want. Right click on the button and choose a different icon.
5. Close the Customize Window.




Then, each time you want to export your mxd data.

2. Create a new empty folder to receive your data.
3. Save your MXD project, using relative paths, to the newly created folder.
4. Run the WriteLayerPaths2TXT   tool, this created a text file in the same folder as the mxd, (as the same name as the mxd) listing the data type, file name, and path to the layers in your mxd.
5.  In Windows Explorer or WinPython, navigate to the mxdexporer.py file and click to run the script.
6. The mxdexporter.py script will prompt you for a path to the file containing the mxd. 
For best luck use the paths as they appear in ArcCatalog since the script is case sensitive.



Know issues and program crashing things.
-This program does not include support for Coverages or CADD layers in your mxd.  Coverages or CADD layers in the mxd will crash the script.  Many other file types have not been tested and may crash the script.

-The folder receiving the data must not contain files with the same name as ones in the mxd.  In other words, the mxdexporter.py will not over-write existing files.

- Running the python script on an mxd that has a red exclamation point for a broken data source will crash the program.

- If you are using this tool on a preexisting mxd document, use caution when running the WriteLayerPaths2TXT tool.  This tool may create the text file in the original mxd location and not you new folder destined to store your data.  If this is the case the python script will crash.  If this happens, restart ArcMap and open the mxd that is in the output folder,  rerun the WriteLayerPaths2TXT tool again before running the python script.




Write with bugs or tips so I can update this help guide.
gerry@gabrisch.us
1-2-07
