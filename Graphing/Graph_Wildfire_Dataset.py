"""

Create plot of Wildfire Severity values and input variables

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

import dask
import pandas as pd
import matplotlib.pyplot as plt
import rasterio
import xarray
import xarray as xr
import rioxarray
import threading
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib_scalebar.scalebar import ScaleBar
from numpy.core._exceptions import _ArrayMemoryError
from pyproj import CRS
from xarray.plot import imshow
from rasterio.plot import show
from xarray.plot import hist
from os import scandir
import geopandas as gpd

input_path = "D:/dNBR/"
input_f81 = "D:/Wildfire_Extracted_v4/242/"
raster = "D:/dNBR.tif"
dem = "D:/unaligned/extent_ProjectRaster_clip.tif"
dem2 = "D:/Wildfire_Extracted_v4/242/242_Elevation.tif"
extent = "D:/Wildfire_Datasets_v8/Area_242.shp"

print("Read Rasters")
# This first section could be rewritten this is a not so good way to do this
with dask.config.set(**{'array.slicing.split_large_chunks': True}):
    combined_ds = []
    with (scandir(input_path) as it):
        for file in it:
            file_name = input_path + file.name
            dr = rioxarray.open_rasterio(file_name, chunks=900, cache=False, lock=threading.Lock(), band_as_variable=True,
                                         mask_and_scale=True)
            dr["band_1"] = dr.band_1 * -1
            dr["band_1"] = dr.band_1.where(dr.band_1.compute() > 100, drop=True)
            combined_ds.append(dr)
        print("Merge Rasters")
        output_ds = xr.merge(combined_ds)

    try:
        print("Export Raster")
        # output_ds.rio.to_raster(raster, tiled=True, windowed=True, lock=threading.Lock())
        # b1 = rasterio.open(raster)
        print("Create Figures")
        fig = plt.figure(figsize=(5.615, 3.152))
        ax2 = fig.add_subplot()
        hist(output_ds.to_array(), ax=ax2, color='lightgrey', edgecolor='black')
        ax2.set_title("")
        ax2.set_xlabel("Wildfire Severity (dNBR)")
        ax2.set_ylabel("Frequency (10$^6$)")

        plt.tight_layout()
        plt.show()

    except _ArrayMemoryError:
        print("Not enough memory!")


print("Read Rasters")
with dask.config.set(**{'array.slicing.split_large_chunks': True}):
    combined_ds = []
    with (scandir(input_f81) as it):
        for file in it:
            file_name = input_f81 + file.name
            dr = rioxarray.open_rasterio(file_name, chunks=900, cache=False, lock=threading.Lock(),
                                         band_as_variable=True,
                                         mask_and_scale=True)
            remove_char = "242_"
            new_name = file.name.replace('.tif', '').replace(remove_char, '', 1)
            name_dict = {'band_1': new_name}
            ds = dr.rename_vars(name_dict=name_dict)

            if new_name == 'dNBR':
                ds['dNBR'] = ds.dNBR * -1

            if new_name == '35_clm':
                ds = ds.rename_vars(name_dict={new_name: 'EBS'})
                ds['EBS'] = ds.EBS * 1000

            if new_name == '7_clm':
                ds = ds.rename_vars(name_dict={new_name: 'ST'})
                ds['ST'] = ds.ST - 273.15

            if new_name == '23_clm':
                ds = ds.rename_vars(name_dict={new_name: 'SRC'})
                ds['SRC'] = ds.SRC * 1000

            if new_name == '33_clm':
                ds = ds.rename_vars(name_dict={new_name: 'SSRD'})
                ds['SSRD'] = ds.SSRD / 1000000

            combined_ds.append(ds)

    try:
        colors = ["darkblue", "lightseagreen", "lawngreen", "gold", "darkgoldenrod", "saddlebrown"]
        cmap1 = LinearSegmentedColormap.from_list("mycmap", colors)
        colors_pre = ["green", "gold", "darkorange", "red"]
        cmap_pre = LinearSegmentedColormap.from_list("mycmappre", colors_pre)
        print("Create Figures")
        fig = plt.figure(figsize=(6.615, 7.552))
        gs = fig.add_gridspec(3, 3)

        print("Plot ax1")
        ax1 = fig.add_subplot(gs[0, 0])
        elev = rasterio.open(dem, crs=CRS.from_epsg(3578))
        # mask = np.ma.masked_where(data > data.min(), data)
        area = gpd.read_file(extent).to_crs('EPSG:3578')
        # plt.imshow(data, cmap='terrain', vmin=280)
        dems = rasterio.plot.show(elev, cmap='terrain', vmin=280, ax=ax1)
        im = dems.get_images()[0]
        # plt.gcf().set_facecolor("white")
        plt.colorbar(im, fraction=0.02, label='Elevation (m)', ax=ax1, location='bottom', orientation='horizontal')
        # rasterio.plot.show(mask, cmap='gist_yarg', ax=ax1)
        area.plot(ax=ax1, color='red')
        ax1.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                        labelleft=False)
        ax1.set_aspect(1)
        ax1.add_artist(ScaleBar(1, location="lower left"))
        ax1.set_title("")
        ax1.set_xlabel("")
        ax1.set_ylabel("")
        ax1.text(0.85, 0.95, "A", transform=ax1.transAxes, fontsize=12, fontweight='bold', va='top')
        print("Plot ax2")
        ax2 = fig.add_subplot(gs[0, 1])
        elev2 = rasterio.open(dem2, crs=CRS.from_epsg(3578))
        dems2 = rasterio.plot.show(elev2, cmap='terrain', vmin=280, ax=ax2)
        im2 = dems2.get_images()[0]
        plt.colorbar(im2, fraction=0.02, label='Elevation (m)', ax=ax2, location='bottom', orientation='horizontal')
        ax2.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                        labelleft=False)
        ax2.set_aspect(1)
        ax2.add_artist(ScaleBar(1, location="lower left"))
        ax2.set_title("")
        ax2.set_xlabel("")
        ax2.set_ylabel("")
        ax2.text(0.9, 0.95, "B", transform=ax2.transAxes, fontsize=12, fontweight='bold', va='top')
        print("Plot ax3")
        ax3 = fig.add_subplot(gs[0, 2])
        imshow(combined_ds[53].dNBR, ax=ax3, add_colorbar=True, cmap=cmap_pre, vmin=0,
               cbar_kwargs={'label': 'dNBR', 'fraction': 0.02, 'norm': LogNorm, 'location': 'bottom',
                            'orientation': 'horizontal'})
        ax3.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                        labelleft=False)
        ax3.set_aspect(1)
        # ax3.add_artist(ScaleBar(1, location="lower left"))
        ax3.set_title("")
        ax3.set_xlabel("")
        ax3.set_ylabel("")
        ax3.text(0.9, 0.95, "C", transform=ax3.transAxes, fontsize=12, fontweight='bold', va='top')
        print("Plot ax4")
        ax4 = fig.add_subplot(gs[1, 0])
        imshow(combined_ds[58].pre, ax=ax4, add_colorbar=True, cmap=cmap1,
               cbar_kwargs={'label': 'Pre-NBR', 'fraction': 0.02, 'norm': LogNorm, 'location': 'bottom',
                            'orientation': 'horizontal'},
               vmin=300, vmax=700)
        ax4.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                        labelleft=False)
        ax4.set_aspect(1)
        # ax4.add_artist(ScaleBar(1, location="lower left"))
        ax4.set_title("")
        ax4.set_xlabel("")
        ax4.set_ylabel("")
        ax4.text(0.9, 0.95, "D", transform=ax4.transAxes, fontsize=12, fontweight='bold', va='top')

        print("Plot ax5")
        ax5 = fig.add_subplot(gs[1, 1])
        imshow(combined_ds[64].VS, ax=ax5, add_colorbar=True, cmap='jet', cbar_kwargs={'label': 'VS', 'fraction': 0.02,
                                                                                       'norm': LogNorm,
                                                                                       'location': 'bottom',
                                                                                       'orientation': 'horizontal'})
        ax5.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                        labelleft=False)
        ax5.set_aspect(1)
        # ax5.add_artist(ScaleBar(1, location="lower left"))
        ax5.set_title("")
        ax5.set_xlabel("")
        ax5.set_ylabel("")
        ax5.text(0.9, 0.95, "E", transform=ax5.transAxes, fontsize=12, fontweight='bold', va='top')
        print("Plot ax6")
        ax6 = fig.add_subplot(gs[1, 2])
        imshow(combined_ds[65].WE, ax=ax6, add_colorbar=True, cmap='jet', cbar_kwargs={'label': 'WE', 'fraction': 0.02,
                                                                                       'norm': LogNorm,
                                                                                       'location': 'bottom',
                                                                                       'orientation': 'horizontal'})
        ax6.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                        labelleft=False)
        ax6.set_aspect(1)
        # ax6.add_artist(ScaleBar(1, location="lower left"))
        ax6.set_title("")
        ax6.set_xlabel("")
        ax6.set_ylabel("")
        ax6.text(0.9, 0.95, "F", transform=ax6.transAxes, fontsize=12, fontweight='bold', va='top')
        print("Plot ax7")
        ax7 = fig.add_subplot(gs[2, 0])
        imshow(combined_ds[27].EBS, ax=ax7, add_colorbar=True, cmap='terrain',
               cbar_kwargs={'label': 'EVT (mm)', 'fraction': 0.02, 'norm': LogNorm, 'location': 'bottom',
                            'orientation': 'horizontal'})
        ax7.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                        labelleft=False)
        ax7.set_aspect(1)
        # ax7.add_artist(ScaleBar(1, location="lower left"))
        ax7.set_title("")
        ax7.set_xlabel("")
        ax7.set_ylabel("")
        ax7.text(0.9, 0.95, "G", transform=ax7.transAxes, fontsize=12, fontweight='bold', va='top')
        print("Plot ax8")
        ax8 = fig.add_subplot(gs[2, 1])
        imshow(combined_ds[47].ST, ax=ax8, add_colorbar=True, cmap='jet',
               cbar_kwargs={'label': 'ST (°C)', 'fraction': 0.02, 'norm': LogNorm, 'location': 'bottom',
                            'orientation': 'horizontal'})
        ax8.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                        labelleft=False)
        ax8.set_aspect(1)
        # ax8.add_artist(ScaleBar(1, location="lower left"))
        ax8.set_title("")
        ax8.set_xlabel("")
        ax8.set_ylabel("")
        ax8.text(0.9, 0.95, "H", transform=ax8.transAxes, fontsize=12, fontweight='bold', va='top')
        print("Plot ax9")
        ax9 = fig.add_subplot(gs[2, 2])
        imshow(combined_ds[14].SRC, ax=ax9, add_colorbar=True, cmap='jet',
               cbar_kwargs={'label': 'SRC (mm)', 'fraction': 0.02,
                            'norm': LogNorm, 'location': 'bottom', 'orientation': 'horizontal'})
        ax9.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                        labelleft=False)
        ax9.set_aspect(1)
        # ax8.add_artist(ScaleBar(1, location="lower left"))
        ax9.set_title("")
        ax9.set_xlabel("")
        ax9.set_ylabel("")
        ax9.text(0.9, 0.95, "I", transform=ax9.transAxes, fontsize=12, fontweight='bold', va='top')

        plt.tight_layout()
        plt.show()

    except _ArrayMemoryError:
        print("Not enough memory!")
