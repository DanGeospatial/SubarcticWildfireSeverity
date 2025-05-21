"""
Improve efficiency by dropping features that are nan error, etc.
Uses output csv files from Compiler.py

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

import numpy as np
import pandas as pd
from os import scandir
from pandas import isnull

input_path = "D:/Wildfire_Compiled_v8/"
datasets_path = "D:/Wildfire_Datasets_v8/wildfire_dataset.csv"
perm_path = "D:/Wildfire_Datasets_v8/wildfire_dataset_xy.csv"
combined_ds = []

# Merge all the csv files into one
with scandir(input_path) as pth:
    for file in pth:
        ds = pd.read_csv(file)
        combined_ds.append(ds)
df = pd.concat(combined_ds)
# df.to_csv(datasets_path, index=False)

# Print column headers
print(df.columns)

# Remove columns that are not needed
error_columns = ['Unnamed: 0', 'spatial_ref']
df.drop(error_columns, axis=1, inplace=True)

# Drop irrelevant features, i.e. lake temperature
irrelevant_columns = ['8_clm', '9_clm', '10_clm', '11_clm', '12_clm', '13_clm', '14_clm', '15_clm', '16_clm', '17_clm',
                      '18_clm', '19_clm', '20_clm', '21_clm', '22_clm', '41_clm']
df.drop(irrelevant_columns, axis=1, inplace=True)

df.dropna(inplace=True)

# Remove no data and Unclassified rows based on LC
df = df[df.LC != 255]
df = df[df.LC != 0]

# Remove nan/no data for all rows
for column in df:
    df = df[df[column] != np.nan]
    df = df[df[column] != np.nan]

# This is redundant
for column in df:
    df = df[df[column] != -3402823e-32]
    df = df[df[column] != -3.4028230000000003e+38]

# Remove water rows
df = df[df.LC != 20]

# Remove glacier/snow rows
df = df[df.LC != 31]

# Remove rock rows
df = df[df.LC != 32]

# Remove unburned rows
df = df[df.dNBR < -100]
df.dNBR = df.dNBR.multiply(-1)
print(df['dNBR'].mean())

# This section is for spatial autocorrelation
# coordinates are removed and then sample.reset_index shuffles data
# then coordinates can be added back or not
todrop = ['x', 'y']
perm = df.drop(todrop, axis=1)
permutated = perm.sample(frac=1, random_state=32).reset_index(drop=True)

# reduced without xy
permutated.to_csv(datasets_path, index=False)

# reduced with xy
dfr = df[['x', 'y']]
dfc = pd.concat([dfr, permutated], axis=1)
dfc.to_csv(perm_path, index=False)

# Print remaining columns and rows
print(permutated.columns)
print(permutated.eq(0).sum().sum())
print(permutated.eq(np.nan).sum().sum())
print(permutated.isnull().sum().sum())
print(permutated.shape)
