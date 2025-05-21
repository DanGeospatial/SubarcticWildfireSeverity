"""
Get all the input raster datasets for each fire in a folder.
Boundaries are clipped to each fire.

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
from Data_Retreival.Topographic import (getAspect, getElevation, getSlope, getTWI, getTPI, getDDG, getDAH, getSVF,
                                        getVD, getVS, getWE, getLSF)
from Data_Retreival.Fire_danger_indices_ERA5 import getERA5L, getClimate, getLAI
from Data_Retreival.Fire_Severity import getdNBR, getmNBR, getpre
from Data_Retreival.Land_Cover import getLCYear

fires = ['81', '326', '162', '109', '83', '228', '113', '227', '157', '115', '64', '174', '170', '233', '243', '58',
         '134', '155', '178', '161', '119', '23', '266', '99', '242', '160', '31', '240', '139', '334', '296', '179',
         '95', '71', '313', '84', '248', '100', '232', '120', '171', '172', '77', '74', '177', '166', '259', '117',
         '239', '82', '199', '167', '148', '152', '142', '298', '66', '249', '131', '87', '260', '146', '230', '268',
         '329', '15', '129', '28', '321', '333']
fire_year = ['1995', '2019', '2004', '1998', '1995', '2009', '1998', '2009', '2004', '1998', '1994', '2004', '2004',
             '2009', '2010', '1994', '1999', '2004', '2004', '2004', '1999', '1990', '2013', '1996', '2010', '2004',
             '1991', '2009', '2001', '2019', '2015', '2004', '1995', '1994', '2017', '1995', '2011', '1996', '2009',
             '1999', '2004', '2004', '1994', '1994', '2004', '2004', '2013', '1998', '2009', '1995', '2006', '2004',
             '2003', '2004', '2002', '2015', '1994', '2011', '1999', '1995', '2013', '2003', '2009', '2013', '2019',
             '1989', '1999', '1990', '2018', '2019']

polygons = "Z:/Research/Masters/5_Extracted/dNBR/Polygons/"
climate_loc = "D:/Wildfire_Climate_Export_v2/"
export_path = "D:/Wildfire_Extracted_v4/"

# Only turn this on if you want to extract climate data
# Right now it is set to fire season
# This function was only used for testing
do_climate = False
if do_climate:
    # Remove duplicate years to speed up processing
    years_trim = list(set(fire_year))
    for year in years_trim:
        getERA5L(year)
        image = climate_loc + year + ".tiff"

# !WARNING!
# !All files must be PERFECTLY aligned before using the remainder of this tool!
# You can use something like: https://www.arcgis.com/home/item.html?id=4f5e9d4e3b974890991d33e7e5251231

# Get all files and place them in the correct directories
for fire in fires:
    # Select fire polygon and naming scheme
    fire_box = polygons + fire + "/" + fire + ".shp"
    save_loc = export_path + fire + "/" + fire
    fire_index = fires.index(fire)
    year_of_fire = fire_year[fire_index]
    # Run through retrieval functions
    # This could be better optimized
    getdNBR(fire_box, fire, save_loc)
    getmNBR(fire_box, save_loc)
    getAspect(fire_box, save_loc)
    getTPI(fire_box, save_loc)
    getTWI(fire_box, save_loc)
    getSlope(fire_box, save_loc)
    getElevation(fire_box, save_loc)
    getLCYear(fire_box, year_of_fire, save_loc)
    getpre(fire_box, year_of_fire, save_loc)
    print("Check getClimate function to choose which average period is extracted")
    getClimate(fire_box, year_of_fire, save_loc)
    getLAI(fire_box, year_of_fire, save_loc)
    getDDG(fire_box, save_loc)
    getDAH(fire_box, save_loc)
    getSVF(fire_box, save_loc)
    getVD(fire_box, save_loc)
    getVS(fire_box, save_loc)
    getWE(fire_box, save_loc)
    getLSF(fire_box, save_loc)
