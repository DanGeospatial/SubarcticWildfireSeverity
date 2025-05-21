"""
This will turn the raster results of Retrieve.py into one csv per fire

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
import xarray as xr
from os import scandir
from osgeo import gdal
from scipy import stats
import numpy as np
import rasterio
import rioxarray

fires = ['81', '326', '162', '109', '83', '228', '113', '227', '157', '115', '64', '174', '170', '233', '243', '58',
         '134', '155', '178', '161', '119', '23', '266', '99', '242', '160', '31', '240', '139', '334', '296', '179',
         '95', '71', '313', '84', '248', '100', '232', '120', '171', '172', '77', '74', '177', '166', '259', '117',
         '239', '82', '199', '167', '148', '152', '142', '298', '66', '249', '131', '87', '260', '146', '230', '268',
         '329', '15', '129', '28', '321', '333']

import_path = "D:/Wildfire_Extracted_v4/"
output_path = "D:/Wildfire_Compiled_v8/"

print("Warning! If your files are not aligned PERFECTLY then this tool will not work properly!")
print(gdal.VersionInfo())


def find_mode(arr, axis):
    m = stats.mode(arr, axis=axis)
    # this function is needed because stats.mode does not return the correct dim
    return m[0]


for fire in fires:
    input_dir = import_path + fire + "/"
    combined_ds = []
    # Get all rasters in each input folder per fire
    with scandir(input_dir) as it:
        for file in it:
            if file.is_file():
                file_name = input_dir + file.name
                # Read raster and set naming
                dr = rioxarray.open_rasterio(file_name, band_as_variable=True, mask_and_scale=True)
                remove_char = fire + "_"
                new_name = file.name.replace('.tif', '').replace(remove_char, '', 1)
                name_dict = {'band_1': new_name}
                ds = dr.rename_vars(name_dict=name_dict)
                # Land Cover is an encoded int, so it needs to use mode
                # coarsen inputs from 30m to 60m
                if new_name == 'LC':
                    ds_coarse = ds.coarsen(x=2, y=2, boundary='pad').reduce(find_mode, keep_attrs=True)
                else:
                    ds_coarse = ds.coarsen(x=2, y=2, boundary='pad').mean()
                combined_ds.append(ds_coarse)
    # Combine all input datasets per fire
    file_out = output_path + fire + ".csv"
    output_ds = xr.merge(combined_ds)
    output_ds.to_dask_dataframe().to_csv(file_out, single_file=True)
