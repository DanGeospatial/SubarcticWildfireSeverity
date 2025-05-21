"""
For plotting a graph of Percentage Land Cover per year
This script was not used!

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

import rioxarray
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
from os import scandir
from numpy.core._exceptions import _ArrayMemoryError

import_path = "I:/LC/aligned/"
output_path = "I:/Wildfire_Datasets_v3.1/LC_year.csv"

input_dir = import_path + "/"
drop_columns = ['spatial_ref']
column_names = [1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
                2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
combined_ds = []
combined_xr = []
grouped_values = []

with scandir(input_dir) as it:
    for file in it:
        if file.is_file():
            if file.name.endswith(".tif"):
                file_name = input_dir + file.name
                dr = rioxarray.open_rasterio(file_name, band_as_variable=True)
                remove_char = "lc_"
                new_name = file.name.replace('.tif', '').replace(remove_char, '', 1)
                name_dict = {'band_1': new_name}
                ds = dr.rename_vars(name_dict=name_dict)
                combined_ds.append(ds)

output_ds = xr.merge(combined_ds)
df = output_ds.to_dataframe()
combined_xr.append(df)
combined_df = pd.concat(combined_xr)

print(combined_df.columns)

# Remove columns that are not needed
combined_df.drop(drop_columns, axis=1, inplace=True)

combined_df = pd.read_csv(output_path)

combined_df = combined_df[combined_df['1986'] != 255]
combined_df = combined_df[combined_df['1986'] != 0]

# This is necessary to help reduce ram usage
row_sample = combined_df.sample(axis=0, n=12000000, random_state=32)

col = {'y1': 1986, 'y2': 1987, 'y3': 1988, 'y4': 1989, 'y5': 1990, 'y6': 1991, 'y7': 1992, 'y8': 1993, 'y9': 1994,
       'y10': 1995, 'y11': 1996, 'y12': 1997, 'y13': 1998, 'y14': 1999, 'y15': 2000, 'y16': 2001, 'y17': 2002,
       'y18': 2003, 'y19': 2004, 'y20': 2005, 'y21': 2006, 'y22': 2007, 'y23': 2008, 'y24': 2009, 'y25': 2010,
       'y26': 2011, 'y27': 2012, 'y28': 2013, 'y29': 2014, 'y30': 2015, 'y31': 2016, 'y32': 2017, 'y33': 2018,
       'y34': 2019}
new_combined = row_sample.assign(**col)
print(new_combined.columns)

new_combined.replace(to_replace=20, value='Water', inplace=True)
new_combined.replace(to_replace=31, value='Snow', inplace=True)
new_combined.replace(to_replace=32, value='Rock', inplace=True)
new_combined.replace(to_replace=33, value='Barren Land', inplace=True)
new_combined.replace(to_replace=40, value='Bryoids', inplace=True)
new_combined.replace(to_replace=50, value='Shrubs', inplace=True)
new_combined.replace(to_replace=80, value='Wetland', inplace=True)
new_combined.replace(to_replace=81, value='Wetland Treed', inplace=True)
new_combined.replace(to_replace=100, value='Herbs', inplace=True)
new_combined.replace(to_replace=210, value='Coniferous', inplace=True)
new_combined.replace(to_replace=220, value='Broad Leaf', inplace=True)
new_combined.replace(to_replace=230, value='Mixedwood', inplace=True)


new_combined.reindex(columns=['y1', '1986', 'y2', '1987', 'y3', '1988', 'y4', '1989', 'y5', '1990', 'y6', '1991', 'y7',
                             '1992', 'y8', '1993', 'y9', '1994', 'y10', '1995', 'y11', '1996', 'y12', '1997', 'y13',
                             '1998', 'y14', '1999', 'y15', '2000', 'y16', '2001', 'y17', '2002', 'y18', '2003', 'y19',
                             '2004', 'y20', '2005', 'y21', '2006', 'y22', '2007', 'y23', '2008', 'y24', '2009', 'y25',
                             '2010', 'y26', '2011', 'y27', '2012', 'y28', '2013', 'y29', '2014', 'y30', '2015', 'y31',
                             '2016', 'y32', '2017', 'y33', '2018', 'y34', '2019'])

dfy = pd.concat([new_combined['y1'], new_combined['y2'], new_combined['y3'], new_combined['y4'], new_combined['y5'],
                 new_combined['y6'], new_combined['y7'], new_combined['y8'], new_combined['y9'], new_combined['y10'],
                 new_combined['y11'], new_combined['y12'], new_combined['y13'], new_combined['y14'], new_combined['y15'],
                 new_combined['y16'], new_combined['y17'], new_combined['y18'], new_combined['y19'], new_combined['y20'],
                 new_combined['y21'], new_combined['y22'], new_combined['y23'], new_combined['y24'], new_combined['y25'],
                 new_combined['y26'], new_combined['y27'], new_combined['y28'], new_combined['y29'], new_combined['y30'],
                 new_combined['y31'], new_combined['y32'], new_combined['y33'], new_combined['y34']], ignore_index=True)
dfv = pd.concat([new_combined['1986'], new_combined['1987'], new_combined['1988'], new_combined['1989'],
                 new_combined['1990'], new_combined['1991'], new_combined['1992'], new_combined['1993'],
                 new_combined['1994'], new_combined['1995'], new_combined['1996'], new_combined['1997'],
                 new_combined['1998'], new_combined['1999'], new_combined['2000'], new_combined['2001'],
                 new_combined['2002'], new_combined['2003'], new_combined['2004'], new_combined['2005'],
                 new_combined['2006'], new_combined['2007'], new_combined['2008'], new_combined['2009'],
                 new_combined['2010'], new_combined['2011'], new_combined['2012'], new_combined['2013'],
                 new_combined['2014'], new_combined['2015'], new_combined['2016'], new_combined['2017'],
                 new_combined['2018'], new_combined['2019']], ignore_index=True)
dfc = pd.concat([dfy, dfv], axis=1)
dfc.rename(columns={0: "Year", 1: "LandCover"}, inplace=True)

try:
    # Calculate percentage table for year LC
    percent = pd.crosstab(dfc['Year'], dfc['LandCover'], normalize='index').mul(100).round(2)
    ax = percent.plot(kind='barh', stacked=True, figsize=(8, 6))

    for c in ax.containers:
        # customize the label to account for cases when there might not be a bar section
        labels = [f'{w:.2f}%' if (w := v.get_width()) > 0 else '' for v in c]

        # set the bar label
        # This is hard to see on small bars
        # ax.bar_label(c, labels=labels, label_type='center')

    ax.legend(bbox_to_anchor=(1, 1.02), loc='upper left')
    ax.set_xlabel("Percentage Land Cover")
    ax.set_ylabel("Year")
    plt.show()
except _ArrayMemoryError:
    print("Out of memory!")
    dfc_sample = combined_df.sample(axis=0, n=1000000, random_state=32)
    # Calculate percentage table for year LC
    percent = pd.crosstab(dfc_sample['Year'], dfc_sample['LandCover'], normalize='index').mul(100).round(2)
    ax = percent.plot(kind='barh', stacked=True, figsize=(8, 6))

    for c in ax.containers:
        # customize the label to account for cases when there might not be a bar section
        labels = [f'{w:.2f}%' if (w := v.get_width()) > 0 else '' for v in c]

        # set the bar label
        # This is hard to see on small bars
        # ax.bar_label(c, labels=labels, label_type='center')

    ax.legend(bbox_to_anchor=(1, 1.02), loc='upper left')
    ax.set_xlabel("Percentage Land Cover")
    ax.set_ylabel("Year")
    plt.show()
