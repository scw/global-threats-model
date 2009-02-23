Import Pour Points
------------------

    v.in.ogr dsn="/mnt/storage/marine_threats/work/raster_stats/workspace/pieces/global_plume_v2_3.shp" output="pours_3" min_area=0.0001 snap=-1

Determine Distance Limit
------------------------

The R script plume_distributions.R was used to figure out the threshold values for different datasets. It reads a DBase (.DBF) file containing the attribute values in question.  The default columns we used for plume modeling were 'SUM_FERTC', 'SUM_PESTC', 'SUM_IMPV'. By determining the distribution of values, we're able to set a reasonable limit on the size of the plume.

This distribution information is then entered inside the getLimit function of plume_buffer.py.

Initial Pluming
---------------

Make sure you have an ocean raster, which is potential area for pluming (ocean cells only):
    g.copy rast=ocean@plume,ocean


Next run the model.  The format is: plume_buffer.py <vector name> <attribute name> where <vector name> is the vector data imported in the first step:
    python plume_buffer.py pours_3 SUM_FERTC

Merging Layers
--------------

This step caused the most headaches. The general process is exporting the many rasters which represent discrete plumes for particular pour points, and combining them into one combined dataset. The script 'grass_add.sh' was our first attempt, and if you're doing a relatively small area, its sufficent though has a long run time. Otherwise, you'll want to use 'plume_add_only.py' in most cases. It just imports the addPlume function within 'plume_buffer2.py', and iterates over the existing grass rasters, exports them to GeoTIFF files, and finally adds them together into a combination raster.

    ~/code/Modeling/Plumes/plume_add_only.py p3_fert fert
