"""
This is for testing and model diagnostics

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

import matplotlib
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from esda.moran import Moran
from libpysal.weights import KNN, DistanceBand, min_threshold_distance, W
from numpy.core._exceptions import _ArrayMemoryError
from xgboost import XGBRegressor, plot_importance
from sklearn.metrics import root_mean_squared_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

importance = False
spatial_residuals_export = False
moran_i = False

v3_059 = "D:/Wildfire_Datasets_v8/wildfire_dataset_xy.csv"

train_ratio = 0.60
validation_ratio = 0.20
test_ratio = 0.20

df = pd.read_csv(v3_059)

y = df["dNBR"]
x = df[["pre", "LC", "46_clm", "tpi", "43_clm", "35_clm", "45_clm", "VS", "WE", "23_clm", "49_clm",
        "Aspect", "33_clm", "38_clm", "50_clm", "7_clm", "42_clm", "DAH"]]

# train is now 60% of the entire data set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1 - train_ratio, random_state=32)

# test is now 20% of the initial data set
# validation is now 20% of the initial data set
x_val, x_test, y_val, y_test = train_test_split(x_test, y_test,
                                                test_size=test_ratio / (test_ratio + validation_ratio), random_state=32)

print(x.head())

# Input testing parameters
regressor = XGBRegressor(objective='reg:squarederror', learning_rate=0.01, n_estimators=1000,
                         early_stopping_rounds=10, random_state=32, min_split_loss=0,
                         max_depth=10, min_child_weight=1, subsample=0.7059719473304258,
                         colsample_bytree=0.8994514591758284, colsample_bylevel=0.8904199797234215,
                         colsample_bynode=0.8754449733223327, reg_lambda=0.016916708991554074,
                         reg_alpha=0.0011336609763898625)

regressor.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_val, y_val)])
print(regressor.best_iteration)

# Load if you only want metrics from pre-trained model
# regressor.load_model("D:/Wildfire_Results_v6/xgb_Ray_H100s.json")
# regressor.save_model("D:/Wildfire_Results_v7/xgb_test.json")

predictions = regressor.predict(x_val)

# Calculate MSE
mse = mean_squared_error(y_val, predictions)
print('Mean Squared Error: ', mse)

# Calculate RMSE
rmse = root_mean_squared_error(y_val, predictions)
print('Root Mean Squared Error: ', rmse)

# Calculate sklearn version of r2
r2 = r2_score(y_val, predictions)
print('r2: ', r2)

# Val %VE (Should be same as r2)
VEV = (1 - (mse / (y_val.var()))) * 100
print('%VE: ', VEV)

# Val %RMSE
P_RMSE = (abs(rmse / (y_val.mean())) * 100)
print('% RMSE: ', P_RMSE)

# Plot default importance metrics. Not as good as SHAP
if importance:
    # Plot the number of times a feature appears in a tree
    plot_importance(regressor, show_values=False, importance_type="gain")
    plt.show()
    # Only plot top 9
    plot_importance(regressor, max_num_features=9, show_values=False, importance_type="gain")
    plt.show()
    # Using weight
    plot_importance(regressor, show_values=False, importance_type="weight")
    plt.show()

# Export model residuals
if spatial_residuals_export:
    predictions_all = regressor.predict(x)
    res = y - predictions_all

    residuals = pd.DataFrame({
        'x': df['x'],
        'y': df['y'],
        'resid': res
    })

    residuals.to_csv("D:/Wildfire_Datasets_v8/resid.csv", index=False)
    print(residuals.head())
    print(residuals.isnull().sum().sum())

# Calculate Moran's I for spatial autocorrelation
# This python library is very slow and uses excessive amounts of memory
# Thus, this section was not used
if moran_i:
    gdf_all = gpd.GeoDataFrame(
        x, geometry=gpd.points_from_xy(x['x'], x['y']), crs="EPSG:3578")

    gdf_array = np.vstack(gdf_all.geometry.apply(lambda p: np.hstack(p.xy)))
    thresholding = min_threshold_distance(gdf_array)
    print(thresholding)

    k = 50
    try:
        # Using knn for spatial weights
        w2 = KNN.from_dataframe(gdf_all, k=k)
        w2.transform = 'R'

        predictions_all = regressor.predict(x)
        # Calculate global moran's I
        moran_all = Moran(y - predictions_all, w=w2, permutations=999)
        print('Morans I: ', moran_all.I)
        print('p-value for Moran: ', moran_all.p_sim)
    except _ArrayMemoryError:
        print(f"Not enough memory for {k}!")


    try:
        # Using DistanceBand for spatial weights
        w2 = DistanceBand.from_dataframe(gdf_all, threshold=thresholding)
        w2.transform = 'R'

        # w2 = W.from_file(weights)

        predictions_all = regressor.predict(x)
        # Calculate global moran's I
        moran_all = Moran(y - predictions_all, w=w2, permutations=999)
        print('Morans I: ', moran_all.I)
        print('p-value for Moran: ', moran_all.p_sim)
    except _ArrayMemoryError:
        print("Not enough memory for Distance!")
