"""
Load land cover

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

# This function clips a dataset to an input area and saves it to the given location
def getLCYear(area, year, savepath):
    # Get LC of year before fire
    year = int(year) - 1
    file_lc = ("D:/Wildfire_Aligned_Rasters_v2/lc_" + str(year) + ".tif")
    save_loc = savepath + "_LC" + ".tif"

    wbt.clip_raster_to_polygon(i=file_lc, polygons=area, output=save_loc)

