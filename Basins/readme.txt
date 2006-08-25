========================
Basin processing scripts
========================

Background
==========

 - These scripts are designed to aid in the `basins generation process`_.
    
 - This code can be checked out at any time via Subversion::

    svn co https://ebm.nceas.ucsb.edu/svn/Modeling/Basins

 - The code can also be `viewed in Trac`_.
    
.. _basins generation process: http://portal.nceas.ucsb.edu/Members/scw/basins-generation-process
.. _viewed in Trac: http://code.nceas.ucsb.edu/browser/Modeling/Basins/

AML Usage
=========

Install ``basingenerate.aml`` into your local Arc installation under:
    <arc root>\atool\grid
    i.e: C:\arcgis\arcexe9x\atool\grid

To run, from the grid prompt run::

    basingenerate DEM <maximum fill depth> <maximum nibble amount> <output>
    i.e: basingenerate dem 100 12 f:\dev\wgs_globe\australia\bump_v2

Python Usage
============

When running the Python scripts, make sure that the interpreter is the same one
ArcGIS recognizes.  ESRI has a document `detailing the process`_.  The scripts
perform the following operations::

    basinBump.py    Rebuild a DEM based on burns, breaks and drains.   
    basinPours.py   Find the pour points for a baisn model
    basinBuild.py   Generate a local 90m SRTM model

.. _detailing the process: http://support.esri.com/index.cfm?fa=knowledgebase.techarticles.articleShow&d=26872

VBA Usage
=========

Open the field calculator: Right click Shapefile, select *Open attribute table*,
right click on the column to be calculated, choose *Calculate values*. From this
field calculator, select *Load...* and chose a .cal file::

    area.cal        Calculate areas, in square kilometers (km^2)
    name_source.cal Choose name source <VMAP, GTN, geonames, manual>
    basin_id.cal    Calculate basin_id column
