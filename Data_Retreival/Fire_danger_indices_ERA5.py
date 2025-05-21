"""
Get climate data with option for download from GEE

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

import os
import ee
import geemap
import whitebox_tools
import PIL.Image as _imaging

url = "https://earthengine-highvolume.googleapis.com"
out_loc = "I:/Wildfire_Climate_Export_v2/"
wbt = whitebox_tools.WhiteboxTools()
wbt.set_whitebox_dir("E:/Users/speed/anaconda3/envs/Yukon_Wildfire_Drivers_v2/Library/bin")

# Initialize Earth Engine Api
# More information at developers.google.com/earth-engine/guides/python_install-conda#windows
ee.Initialize(project='ee-nelson-remote-sensing', url=url)


def getERA5L(year):
    """
    This function was intended to get ERA5 Data from GEE for each year.

    :param year: year of climate data retrieval
    :return: nan
    """

    boundary = ee.FeatureCollection("users/danielnelsonca/Projects/Arctic_Ecozones_in_Canada")
    area = ee.FeatureCollection("users/danielnelsonca/MastersThesis/FinalSiteArea")
    extent = area.geometry().bounds()

    start_date = year + "-" + "05"
    end_date = year + "-" + "09"
    output = out_loc + year + ".tiff"

    dataset = (ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR")
               .filter(ee.Filter.date(start_date, end_date))
               .filterBounds(boundary))

    average = dataset.reduce(ee.Reducer.mean()).clip(boundary)

    geemap.download_ee_image(image=average, filename=output, scale=11132, crs="EPSG:3578", region=extent)


def getClimate(area, year, savepath):
    # This function is for yearly or seasonally averaged data
    # - 3 for 3y average before fire or different times
    # year = year for current fire season

    year = int(year)
    # year = year - 3

    bands = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
             26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]

    for band in bands:
        # + "_rs" not needed anymore
        output_b = "D:/Wildfire_Aligned_Rasters_v2/v3_cy_rc/average_" + str(year) + "_" + str(band) + ".tif"
        save_loc = savepath + "_" + str(band) + "_clm" + ".tif"

        wbt.clip_raster_to_polygon(i=output_b, polygons=area, output=save_loc)


def getLAI(area, year, savepath):
    # This function is for yearly or seasonally averaged LAI data
    # - 1 for year before fire

    year = int(year) - 1

    bands = [49, 50]

    for band in bands:
        # + "_rs" not needed anymore
        output_b = "D:/Wildfire_Aligned_Rasters_v2/v3_cy_rc/average_" + str(year) + "_" + str(band) + ".tif"
        save_loc = savepath + "_" + str(band) + "_clm" + ".tif"

        wbt.clip_raster_to_polygon(i=output_b, polygons=area, output=save_loc)
