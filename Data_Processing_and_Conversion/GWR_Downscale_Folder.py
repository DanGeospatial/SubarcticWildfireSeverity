"""
This function is designed to perform GWR using SAGA GIS and Arcpy.
It can take custom predictors and loops through all rasters in a folder.

Copyright (C) 2025 Daniel Nelson
Copyright (C) 2025 Yuhong He
Copyright (C) 2025 G.W.K. Moore

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""


import arcpy
arcpy.ImportToolbox("C:/Program Files/saga-8.5.0_x64/ArcSAGA Toolboxes/Spatial and Geostatistics - Regression.pyt", "saga")

# Load predictors
dem = "D:/Wildfire_Aligned_Rasters_v2/Yukon_Elev_no_sinks_Resample.tif"
slope = "D:/Wildfire_Aligned_Rasters_v2/Slope_clip_Resample.tif"
aspect = "D:/Wildfire_Aligned_Rasters_v2/Aspect_clip_Resample.tif"
# Set workspace to find rasters
arcpy.env.workspace = "E:/Temp/flat"
# List all rasters in workspace
rasters = arcpy.ListRasters()

for raster in rasters:
    # Currently set for climate data
    output_getname = str(raster).replace('.tif', '')
    outputRaster = "D:/resample/" + output_getname + ".tif"
    output_res = "D:/resample/" + output_getname + "_res" + ".tif"
    output_q = "D:/resample/" + output_getname + "_q" + ".tif"
    # split parts of each filname
    year = output_getname.replace('average_', '')
    head, sep, tail = year.partition('_')
    # Use tail to get climate band number
    # Not interested in anything above band 50
    if int(tail) > 50:
        continue
    # get nbr/ndvi for given year found in head
    nbr = "D:/nbr_fix/NBR_Fitted_" + head + ".tif"
    # list all PREDICTORS
    pred = [dem, slope, aspect, nbr]
    
    try:
        # https://saga-gis.sourceforge.io/saga_tool_doc/6.1.0/statistics_regression_14.html
        arcpy.saga.tool_14(PREDICTORS=pred, REGRESSION=outputRaster, DEPENDENT=raster, QUALITY=output_q, RESIDUALS=output_res)
    except IndexError:
        pass