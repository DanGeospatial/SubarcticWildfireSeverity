"""
Create SHAP plots

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

import math
import pandas as pd
import mpl_scatter_density
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

shap_data = "D:/Wildfire_Datasets_v8/gpu_shap_df_lc.csv"

shap_df = pd.read_csv(shap_data)

drop_columns = ['Unnamed: 0', 'row_id']
fv_columns = ['shap_values']
sv_columns = ['feature_value']
LC_columns = ['count']
color = '#88c999'
shap_df.drop(drop_columns, axis=1, inplace=True)

fv_df = shap_df.drop(fv_columns, axis=1)
sv_df = shap_df.drop(sv_columns, axis=1)

fv_df.insert(0, 'count', fv_df.groupby('feature').cumcount())
sv_df.insert(0, 'count', sv_df.groupby('feature').cumcount())

fv_pivot = fv_df.pivot(index='count', columns='feature', values='feature_value')
sv_pivot = sv_df.pivot(index='count', columns='feature', values='shap_values')

# Fix LC Labels
fv_pivot['LC'].replace(to_replace=33, value='Barren Land', inplace=True)
fv_pivot['LC'].replace(to_replace=40, value='Bryoids', inplace=True)
fv_pivot['LC'].replace(to_replace=50, value='Shrubs', inplace=True)
fv_pivot['LC'].replace(to_replace=80, value='Wetland', inplace=True)
fv_pivot['LC'].replace(to_replace=81, value='Wetland Treed', inplace=True)
fv_pivot['LC'].replace(to_replace=100, value='Herbs', inplace=True)
fv_pivot['LC'].replace(to_replace=210, value='Coniferous', inplace=True)
fv_pivot['LC'].replace(to_replace=220, value='Broad Leaf', inplace=True)
fv_pivot['LC'].replace(to_replace=230, value='Mixedwood', inplace=True)

# Transform LC data for boxplot
sv_lc = sv_pivot['LC'].rename('SV')
LC_con = pd.concat([fv_pivot['LC'], sv_lc], axis=1)
LC_con.insert(0, 'count', LC_con.groupby('LC').cumcount())
LC_pivot = LC_con.pivot(index='count', columns='LC', values='SV')

# Convert Units and Scaling for Graphing
fv_pivot['7_clm'] = fv_pivot['7_clm'].subtract(273.15)

# Scale from m to mm
fv_pivot['42_clm'] = fv_pivot['42_clm'].mul(1000)
fv_pivot['43_clm'] = fv_pivot['43_clm'].mul(1000)
fv_pivot['23_clm'] = fv_pivot['23_clm'].mul(1000)
fv_pivot['35_clm'] = fv_pivot['35_clm'].mul(1000)
fv_pivot['38_clm'] = fv_pivot['38_clm'].mul(1000)

# Scale by 10^6
fv_pivot['33_clm'] = fv_pivot['33_clm'].div(1000000)

# Radians to degrees
# fv_pivot['Slope'] = fv_pivot['Slope'].mul(180 / math.pi)

# Remove extreme outliers
def clean_frame(df: pd.DataFrame):
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
    return df


# Take iqr for better plotting
pre = pd.DataFrame({
    "x": fv_pivot['pre'],
    "y": sv_pivot['pre']
})
pre_q = clean_frame(pre)

NW = pd.DataFrame({
    "x": fv_pivot['46_clm'],
    "y": sv_pivot["46_clm"]
})
NW_q = clean_frame(NW)

TPI = pd.DataFrame({
    "x": fv_pivot['tpi'],
    "y": sv_pivot["tpi"]
})
TPI_q = clean_frame(TPI)

SR = pd.DataFrame({
    "x": fv_pivot['43_clm'],
    "y": sv_pivot["43_clm"]
})
SR_q = clean_frame(SR)

SSR = pd.DataFrame({
    "x": fv_pivot['42_clm'],
    "y": sv_pivot["42_clm"]
})
SSR_q = clean_frame(SSR)

EW = pd.DataFrame({
    "x": fv_pivot['45_clm'],
    "y": sv_pivot["45_clm"]
})
EW_q = clean_frame(EW)

Aspect = pd.DataFrame({
    "x": fv_pivot['Aspect'],
    "y": sv_pivot["Aspect"]
})
Aspect_q = clean_frame(Aspect)

SSRD = pd.DataFrame({
    "x": fv_pivot['33_clm'],
    "y": sv_pivot["33_clm"]
})
SSRD_q = clean_frame(SSRD)

SRC = pd.DataFrame({
    "x": fv_pivot['23_clm'],
    "y": sv_pivot["23_clm"]
})
SRC_q = clean_frame(SRC)

EVT = pd.DataFrame({
    "x": fv_pivot['38_clm'],
    "y": sv_pivot["38_clm"]
})
EVT_q = clean_frame(EVT)

EBS = pd.DataFrame({
    "x": fv_pivot['35_clm'],
    "y": sv_pivot["35_clm"]
})
EBS_q = clean_frame(EBS)

LAIL = pd.DataFrame({
    "x": fv_pivot['50_clm'],
    "y": sv_pivot["50_clm"]
})
LAIL_q = clean_frame(LAIL)

ST = pd.DataFrame({
    "x": fv_pivot['7_clm'],
    "y": sv_pivot["7_clm"]
})
ST_q = clean_frame(ST)

VS = pd.DataFrame({
    "x": fv_pivot['VS'],
    "y": sv_pivot["VS"]
})
VS_q = clean_frame(VS)

WE = pd.DataFrame({
    "x": fv_pivot['WE'],
    "y": sv_pivot["WE"]
})
WE_q = clean_frame(WE)

LAIH = pd.DataFrame({
    "x": fv_pivot['49_clm'],
    "y": sv_pivot["49_clm"]
})
LAIH_q = clean_frame(LAIH)

DAH = pd.DataFrame({
    "x": fv_pivot['DAH'],
    "y": sv_pivot["DAH"]
})
DAH_q = clean_frame(DAH)

# "Viridis-like" colormap with white background
white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
    '#ffffff',
    '#440053',
    '#404388',
    '#2a788e',
    '#21a784',
    '#78d151',
    '#fde624',
], N=256)

# Create group
fig = plt.figure(figsize=(6.615, 7.552))
gs = fig.add_gridspec(4, 2)

ax1 = fig.add_subplot(gs[0, 0], projection='scatter_density')
a1 = ax1.scatter_density(pre_q["x"], pre_q["y"], cmap=white_viridis)
fig.colorbar(a1, ax=ax1, orientation='vertical')
ax1.set_xlabel("Pre-NBR")
ax1.hlines(0, xmax=pre_q["x"].max(), xmin=pre_q["x"].min(), color="tab:grey", linestyles='dashed')
ax1.text(0.05, 0.95, "A", transform=ax1.transAxes, fontsize=12, fontweight='bold', va='top')

ax2 = fig.add_subplot(gs[0, 1], projection='scatter_density')
a2 = ax2.scatter_density(SRC_q['x'], SRC_q['y'], cmap=white_viridis)
fig.colorbar(a2, ax=ax2, orientation='vertical')
ax2.set_xlabel("SRC (mm)")
ax2.hlines(0, xmax=SRC_q['x'].max(), xmin=SRC_q['x'].min(), color="tab:grey", linestyles='dashed')
ax2.text(0.05, 0.95, "B", transform=ax2.transAxes, fontsize=12, fontweight='bold', va='top')

ax3 = fig.add_subplot(gs[1, 0], projection='scatter_density')
a3 = ax3.scatter_density(EBS_q['x'], EBS_q['y'], cmap=white_viridis)
fig.colorbar(a3, ax=ax3, orientation='vertical')
ax3.set_xlabel("EVT (mm)")
ax3.hlines(0, xmax=EBS_q['x'].max(), xmin=EBS_q['x'].min(), color="tab:grey", linestyles='dashed')
ax3.text(0.05, 0.95, "C", transform=ax3.transAxes, fontsize=12, fontweight='bold', va='top')

ax4 = fig.add_subplot(gs[1, 1], projection='scatter_density')
a4 = ax4.scatter_density(ST_q['x'], ST_q['y'], cmap=white_viridis)
fig.colorbar(a4, ax=ax4, orientation='vertical')
ax4.set_xlabel("ST (°C)")
ax4.hlines(0, xmax=ST_q['x'].max(), xmin=ST_q['x'].min(), color="tab:grey", linestyles='dashed')
ax4.text(0.05, 0.95, "D", transform=ax4.transAxes, fontsize=12, fontweight='bold', va='top')

ax5 = fig.add_subplot(gs[2, 0], projection='scatter_density')
a5 = ax5.scatter_density(WE_q['x'], WE_q['y'], cmap=white_viridis)
fig.colorbar(a5, ax=ax5, orientation='vertical')
ax5.set_xlabel("WE")
ax5.hlines(0, xmax=WE_q['x'].max(), xmin=WE_q['x'].min(), color="tab:grey", linestyles='dashed')
ax5.text(0.05, 0.95, "E", transform=ax5.transAxes, fontsize=12, fontweight='bold', va='top')

ax6 = fig.add_subplot(gs[2, 1], projection='scatter_density')
a6 = ax6.scatter_density(SR_q['x'], SR_q['y'], cmap=white_viridis)
fig.colorbar(a6, ax=ax6, orientation='vertical')
ax6.set_xlabel("SR (mm)")
ax6.hlines(0, xmax=SR_q['x'].max(), xmin=SR_q['x'].min(), color="tab:grey", linestyles='dashed')
ax6.text(0.05, 0.95, "F", transform=ax6.transAxes, fontsize=12, fontweight='bold', va='top')

ax7 = fig.add_subplot(gs[3, 0], projection='scatter_density')
a7 = ax7.scatter_density(NW_q['x'], NW_q['y'], cmap=white_viridis)
fig.colorbar(a7, ax=ax7, orientation='vertical')
ax7.set_xlabel("NW (m/s)")
ax7.hlines(0, xmax=NW_q['x'].max(), xmin=NW_q['x'].min(), color="tab:grey", linestyles='dashed')
ax7.text(0.05, 0.95, "G", transform=ax7.transAxes, fontsize=12, fontweight='bold', va='top')

ax8 = fig.add_subplot(gs[3, 1], projection='scatter_density')
a8 = ax8.scatter_density(VS_q["x"], VS_q['y'], cmap=white_viridis)
fig.colorbar(a8, ax=ax8, orientation='vertical')
ax8.set_xlabel("VS")
ax8.hlines(0, xmax=VS_q["x"].max(), xmin=VS_q["x"].min(), color="tab:grey", linestyles='dashed')
ax8.text(0.05, 0.95, "H", transform=ax8.transAxes, fontsize=12, fontweight='bold', va='top')

fig.supylabel("SHAP Values")
plt.tight_layout()
plt.show()

# Create group 2
fig = plt.figure(figsize=(6.615, 7.552))
gs = fig.add_gridspec(4, 2)

ax1 = fig.add_subplot(gs[0, 0], projection='scatter_density')
a1 = ax1.scatter_density(SSRD_q['x'], SSRD_q['y'], cmap=white_viridis)
fig.colorbar(a1, ax=ax1, orientation='vertical')
ax1.set_xlabel("SSRD (J/m$^2$ 10$^6$)")
ax1.hlines(0, xmax=SSRD_q['x'].max(), xmin=SSRD_q['x'].min(), color="tab:grey", linestyles='dashed')
ax1.text(0.05, 0.95, "A", transform=ax1.transAxes, fontsize=12, fontweight='bold', va='top')

ax2 = fig.add_subplot(gs[0, 1], projection='scatter_density')
a2 = ax2.scatter_density(EW_q['x'], EW_q['y'], cmap=white_viridis)
fig.colorbar(a2, ax=ax2, orientation='vertical')
ax2.set_xlabel("EW (m/s)")
ax2.hlines(0, xmax=EW_q['x'].max(), xmin=EW_q['x'].min(), color="tab:grey", linestyles='dashed')
ax2.text(0.05, 0.95, "B", transform=ax2.transAxes, fontsize=12, fontweight='bold', va='top')

ax3 = fig.add_subplot(gs[1, 0], projection='scatter_density')
a3 = ax3.scatter_density(EVT_q['x'], EVT_q['y'], cmap=white_viridis)
fig.colorbar(a3, ax=ax3, orientation='vertical')
ax3.set_xlabel("EOS (mm)")
ax3.hlines(0, xmax=EVT_q['x'].max(), xmin=EVT_q['x'].min(), color="tab:grey", linestyles='dashed')
ax3.text(0.05, 0.95, "C", transform=ax3.transAxes, fontsize=12, fontweight='bold', va='top')

ax4 = fig.add_subplot(gs[1, 1], projection='scatter_density')
a4 = ax4.scatter_density(SSR_q['x'], SSR_q['y'], cmap=white_viridis)
fig.colorbar(a4, ax=ax4, orientation='vertical')
ax4.set_xlabel("SSR (mm)")
ax4.hlines(0, xmax=SSR_q['x'].max(), xmin=SSR_q['x'].min(), color="tab:grey", linestyles='dashed')
ax4.text(0.05, 0.95, "D", transform=ax4.transAxes, fontsize=12, fontweight='bold', va='top')

ax5 = fig.add_subplot(gs[2, 0], projection='scatter_density')
a5 = ax5.scatter_density(LAIL_q['x'], LAIL_q['y'], cmap=white_viridis)
fig.colorbar(a5, ax=ax5, orientation='vertical')
ax5.set_xlabel("LAI-L")
ax5.hlines(0, xmax=LAIL_q['x'].max(), xmin=LAIL_q['x'].min(), color="tab:grey", linestyles='dashed')
ax5.text(0.05, 0.95, "E", transform=ax5.transAxes, fontsize=12, fontweight='bold', va='top')

ax6 = fig.add_subplot(gs[2, 1], projection='scatter_density')
a6 = ax6.scatter_density(TPI_q['x'], TPI_q['y'], cmap=white_viridis)
fig.colorbar(a6, ax=ax6, orientation='vertical')
ax6.set_xlabel("TPI")
ax6.hlines(0, xmax=TPI_q['x'].max(), xmin=TPI_q['x'].min(), color="tab:grey", linestyles='dashed')
ax6.text(0.05, 0.95, "F", transform=ax6.transAxes, fontsize=12, fontweight='bold', va='top')

ax7 = fig.add_subplot(gs[3, 0], projection='scatter_density')
a7 = ax7.scatter_density(LAIH_q['x'], LAIH_q['y'], cmap=white_viridis)
fig.colorbar(a7, ax=ax7, orientation='vertical')
ax7.set_xlabel("LAI-H")
ax7.hlines(0, xmax=LAIH_q['x'].max(), xmin=LAIH_q['x'].min(), color="tab:grey", linestyles='dashed')
ax7.text(0.05, 0.95, "G", transform=ax7.transAxes, fontsize=12, fontweight='bold', va='top')

ax8 = fig.add_subplot(gs[3, 1], projection='scatter_density')
a8 = ax8.scatter_density(DAH_q['x'], DAH_q['y'], cmap=white_viridis)
fig.colorbar(a8, ax=ax8, orientation='vertical')
ax8.set_xlabel("DAH")
ax8.hlines(0, xmax=DAH_q['x'].max(), xmin=DAH_q['x'].min(), color="tab:grey", linestyles='dashed')
ax8.text(0.05, 0.95, "H", transform=ax8.transAxes, fontsize=12, fontweight='bold', va='top')

fig.supylabel("SHAP Values")
plt.tight_layout()
plt.show()


# take the mean absolute value of the SHAP values for each feature
importance_table = pd.DataFrame({
    'feature': (["Pre", "DAH", "LC", "NW", "TPI", "VS", "SR", "WE", "EVT", "EW", "SRC",
                 "SSRD", "SSR", "EOS", "LAI-L", "ST", "LAI-H", "Aspect"]),
    'value': ([sv_pivot['pre'].abs().mean(), sv_pivot['DAH'].abs().mean(), sv_pivot['LC'].abs().mean(),
               sv_pivot['46_clm'].abs().mean(), sv_pivot['tpi'].abs().mean(), sv_pivot['VS'].abs().mean(),
               sv_pivot['43_clm'].abs().mean(), sv_pivot['WE'].abs().mean(), sv_pivot['35_clm'].abs().mean(),
               sv_pivot['45_clm'].abs().mean(), sv_pivot['23_clm'].abs().mean(), sv_pivot['33_clm'].abs().mean(),
               sv_pivot['42_clm'].abs().mean(), sv_pivot['38_clm'].abs().mean(), sv_pivot['50_clm'].abs().mean(),
               sv_pivot['7_clm'].abs().mean(), sv_pivot['49_clm'].abs().mean(), sv_pivot['Aspect'].abs().mean()])
})

print(importance_table.head())

ordered_df = importance_table.sort_values(by='value')
my_range = range(1, len(importance_table.index) + 1)

fig = plt.figure(figsize=(6.615, 4.815))
gs = fig.add_gridspec(1, 2)

ax1 = fig.add_subplot(gs[0, 0])
ax1.grid(which="major", axis="x")
ax1.hlines(y=my_range, xmin=0, xmax=ordered_df['value'], color='darkgrey', alpha=0.4)
ax1.scatter(ordered_df['value'], my_range, color='peru', s=70, alpha=1, edgecolors="black")
ax1.set_yticks(my_range, ordered_df['feature'], fontsize=8)
ax1.set_xlabel('Mean |SHAP| Value')
ax1.set_ylabel('Variable')
ax1.text(0.05, 0.95, "A", transform=ax1.transAxes, fontsize=12, fontweight='bold', va='top')

ax2 = fig.add_subplot(gs[0, 1])
db_lc = LC_pivot.boxplot(vert=False, ax=ax2, grid=False, color='tan', showfliers=True)
ax2.set_xlabel("SHAP value for Land Cover")
ax2.text(0.05, 0.95, "B", transform=ax2.transAxes, fontsize=12, fontweight='bold', va='top')

plt.tight_layout()
plt.show()
