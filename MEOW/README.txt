MEOW Random Sampling
====================

The general approach:
 - rasterize the MEOW file into distinct rasters per-ecoregion, by:
    + vectorizing a particular ecoregion (so we can calculate the bounding box)
    + rasterize the resulting ecoregion
 - for each rasterized ecoregion, find the # of data cells
 - data cells - null cells x .05 = cells to sample
 - use r.random to select 5% intervals of cells from 5%-95%
 - r.sum for each interval of cells to get cumulative value, divide by the total number of cells in the random sample

meow_ecoregion_stats.py: all raster inputs are defined in getOpts(). The 'threat raster' can be changed, but make sure that the land is NULL, or the calculations can be erroneous. The 'prefix' variable defines how output rasters are prefixed, e.g. 'meow_ecoregion_20001_5pct'. To rerun the script without reusing the existing randomizations, delete all files with the prefix in question, e.g. 'g.mremove rast="meow_ecoregion*"'.

