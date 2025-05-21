"""
Wildfire NBR was calculated using LandTrendR from Landsat

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
def getdNBR(area, fire_id, savepath):
    file_dnbr = ("D:/Wildfire_Aligned_Rasters_v2/" + "dNBR_" + fire_id + ".tif")
    save_loc = savepath + "_dNBR" + ".tif"

    wbt.clip_raster_to_polygon(i=file_dnbr, polygons=area, output=save_loc)


def getmNBR(area, savepath):
    file_dnbr = ("D:/Wildfire_Aligned_Rasters_v2/" + "mNBR" + ".tif")
    save_loc = savepath + "_mNBR" + ".tif"

    wbt.clip_raster_to_polygon(i=file_dnbr, polygons=area, output=save_loc)


def getpre(area, year, savepath):
    year = int(year)
    year = year - 1
    file_pre = ("D:/Wildfire_Aligned_Rasters_v2/NBR_Fitted_" + str(year) + ".tif")
    save_loc = savepath + "_pre" + ".tif"

    wbt.clip_raster_to_polygon(i=file_pre, polygons=area, output=save_loc)
