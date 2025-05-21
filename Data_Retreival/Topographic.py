"""
These have been calculated locally using SAGA GIS for the entire Yukon

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

import whitebox_tools

wbt = whitebox_tools.WhiteboxTools()
# Set this to your whitebox location
wbt.set_whitebox_dir("E:/Users/speed/anaconda3/envs/Yukon_Wildfire_Drivers_v2/Library/bin")

# These functions clip each dataset to an input area and save it to the given location
def getAspect(area, savepath):
    file_aspect = "D:/Wildfire_Aligned_Rasters_v2/Aspect_clip_Resample.tif"
    save_loc = savepath + "_Aspect" + ".tif"

    wbt.clip_raster_to_polygon(i=file_aspect, polygons=area, output=save_loc)


def getElevation(area, savepath):
    file_elevation = "D:/Wildfire_Aligned_Rasters_v2/Yukon_Elev_no_sinks_Resample.tif"
    save_loc = savepath + "_Elevation" + ".tif"

    wbt.clip_raster_to_polygon(i=file_elevation, polygons=area, output=save_loc)


def getSlope(area, savepath):
    file_slope = "D:/Wildfire_Aligned_Rasters_v2/Slope_clip_Resample.tif"
    save_loc = savepath + "_Slope" + ".tif"

    wbt.clip_raster_to_polygon(i=file_slope, polygons=area, output=save_loc)


def getTWI(area, savepath):
    file_twi = "D:/Wildfire_Aligned_Rasters_v2/TopographicWetnessIndex_clip_Resample.tif"
    save_loc = savepath + "_twi" + ".tif"

    wbt.clip_raster_to_polygon(i=file_twi, polygons=area, output=save_loc)


def getTPI(area, savepath):
    file_tpi = "D:/Wildfire_Aligned_Rasters_v2/TopographicPositionIndex_clip_resample.tif"
    save_loc = savepath + "_tpi" + ".tif"

    wbt.clip_raster_to_polygon(i=file_tpi, polygons=area, output=save_loc)


def getDDG(area, savepath):
    file_elevation = "D:/Wildfire_Aligned_Rasters_v2/Gradient.tif"
    save_loc = savepath + "_DDG" + ".tif"

    wbt.clip_raster_to_polygon(i=file_elevation, polygons=area, output=save_loc)


def getDAH(area, savepath):
    file_elevation = "D:/Wildfire_Aligned_Rasters_v2/DiurnalAnisotropicHeating.tif"
    save_loc = savepath + "_DAH" + ".tif"

    wbt.clip_raster_to_polygon(i=file_elevation, polygons=area, output=save_loc)


def getSVF(area, savepath):
    file_elevation = "D:/Wildfire_Aligned_Rasters_v2/SkyViewFactor.tif"
    save_loc = savepath + "_SVF" + ".tif"

    wbt.clip_raster_to_polygon(i=file_elevation, polygons=area, output=save_loc)


def getVD(area, savepath):
    file_elevation = "D:/Wildfire_Aligned_Rasters_v2/ValleyDepth.tif"
    save_loc = savepath + "_VD" + ".tif"

    wbt.clip_raster_to_polygon(i=file_elevation, polygons=area, output=save_loc)


def getVS(area, savepath):
    file_elevation = "D:/Wildfire_Aligned_Rasters_v2/VisibleSky.tif"
    save_loc = savepath + "_VS" + ".tif"

    wbt.clip_raster_to_polygon(i=file_elevation, polygons=area, output=save_loc)


def getWE(area, savepath):
    file_elevation = "D:/Wildfire_Aligned_Rasters_v2/WindExposition.tif"
    save_loc = savepath + "_WE" + ".tif"

    wbt.clip_raster_to_polygon(i=file_elevation, polygons=area, output=save_loc)


def getLSF(area, savepath):
    file_elevation = "D:/Wildfire_Aligned_Rasters_v2/LSFactor.tif"
    save_loc = savepath + "_LSF" + ".tif"

    wbt.clip_raster_to_polygon(i=file_elevation, polygons=area, output=save_loc)