"""
Create plot of study area and bar plots for Burned Area and Fire Season

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

import rasterio
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib_scalebar.scalebar import ScaleBar

# Load existing shapefiles of the Yukon
study_area = "Z:/Research/Masters/4_Model_Files/Reference/AOI/FinalSiteArea.shp"
canada = "Z:/Research/Masters/4_Model_Files/Reference/Canada/Canada.shp"
yukon = "Z:/Research/Masters/4_Model_Files/Reference/Yukon/Yukon_Project.shp"
city = "Z:/Research/Masters/4_Model_Files/Reference/Communities/Yukon_Communities_Project_Main.shp"

dem = "D:/unaligned/extent_ProjectRaster_clip.tif"
lc_19 = "D:/LC/trimed/lc_2019.tif"

stats_fire = "D:/Wildfire_Datasets_v8/stats_ba_fsn.csv"

stats = pd.read_csv(stats_fire)

can = gpd.read_file(canada)
area = gpd.read_file(study_area)
ykt = gpd.read_file(yukon)
# .to_crs('EPSG:5937')
towns = gpd.read_file(city)

elev = rasterio.open(dem)
data = elev.read(1)
mask = np.ma.masked_where(data > data.min(), data)

# Create plot for study area
fig = plt.figure(figsize=(6.615, 4.552))
gs = fig.add_gridspec(2, 2)

ax1 = fig.add_subplot(gs[0, 0])
can.plot(ax=ax1, color='lightgrey')
ykt.plot(ax=ax1, color='wheat')
ax1.add_artist(ScaleBar(1, location="lower right"))
ax1.set_title("")
ax1.set_xlabel("")
ax1.set_ylabel("")
ax1.tick_params(axis='both', which='both', bottom=False, top=False, left=False, labelbottom=False,
                labelleft=False)
ax1.text(0.05, 0.95, "A", transform=ax1.transAxes, fontsize=12, fontweight='bold', va='top')

ax2 = fig.add_subplot(gs[1, 0])
ykt.plot(ax=ax2, color='wheat')
area.plot(ax=ax2, column='ECOREGION', cmap='tab20b', legend=True, legend_kwds={'draggable': True, 'prop': {'size': 7}})
# leg1 = ax2.get_legend()
# towns.plot(ax=ax2, column='PLACE_NAME', cmap='Set1', legend=True,
#           legend_kwds={'loc': 'upper right', 'draggable': True})
# ax2.add_artist(leg1)
ax2.add_artist(ScaleBar(1, location="lower right"))
ax2.set_title("")
ax2.set_xlabel("")
ax2.set_ylabel("")
ax2.tick_params(axis='both', which='both', bottom=False, top=False, left=False, labelbottom=False,
                labelleft=False)
ax2.text(0.05, 0.95, "B", transform=ax2.transAxes, fontsize=12, fontweight='bold', va='top')
ax2.set_ymargin(0.1)
ax2.set_xmargin(0.35)

ax3 = fig.add_subplot(gs[:, 1])
plt.imshow(data, cmap='terrain', vmin=280)
plt.gcf().set_facecolor("white")
plt.colorbar(fraction=0.05, label='Elevation (m)', ax=ax3)
plt.imshow(mask, cmap='gist_yarg')
ax3.add_artist(ScaleBar(1, location="lower left"))
ax3.set_title("")
ax3.set_xlabel("")
ax3.set_ylabel("")
ax3.tick_params(axis='both', which='both', bottom=False, top=False, left=False, labelbottom=False,
                labelleft=False)
ax3.text(0.90, 0.95, "C", transform=ax3.transAxes, fontsize=12, fontweight='bold', va='top')

plt.tight_layout()
plt.show()

# Create plots of Burned Area and Fire Season
fig = plt.figure(figsize=(6.615, 4.152))
gs = fig.add_gridspec(2, 1)

ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(stats['A_KM'], color='lightgrey', bins='auto', edgecolor='black')
ax1.set_xlabel("Burned Area (km$^2$)")
ax1.set_ylabel('Number of Wildfires')
ax1.set_title("")
ax1.text(0.95, 0.95, "A", transform=ax1.transAxes, fontsize=12, fontweight='bold', va='top')

ax2 = fig.add_subplot(gs[1, 0])
ax2.bar(x=stats['Year'], height=stats['Count'], color='lightgrey', edgecolor='black')
ax2.set_xlabel("Fire Season (Year)")
ax2.set_ylabel('Number of Wildfires')
plt.xticks(np.arange(min(stats['Year']), (max(stats['Year'] + 1)), step=2), rotation='vertical')
ax2.set_title("")
ax2.text(0.95, 0.95, "B", transform=ax2.transAxes, fontsize=12, fontweight='bold', va='top')

plt.tight_layout()
plt.show()
