"""
Calculate SHAP values on GPU for massive performance boost

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
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
import xgboost as xgb
import pandas as pd
import shap
import numpy as np

v3_059 = "D:/Wildfire_Datasets_v8/wildfire_dataset.csv"

train_ratio = 0.60
validation_ratio = 0.20
test_ratio = 0.20

print("Reading Dataset")
df = pd.read_csv(v3_059)

y = df["dNBR"]
x = df[["pre", "LC", "46_clm", "tpi", "43_clm", "35_clm", "45_clm", "VS", "WE", "23_clm", "49_clm",
        "Aspect", "33_clm", "38_clm", "50_clm", "7_clm", "42_clm", "DAH"]]

print("Splitting Data")
# train is now 60% of the entire data set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1 - train_ratio, random_state=32)

# test is now 20% of the initial data set
# validation is now 20% of the initial data set
x_val, x_test, y_val, y_test = train_test_split(x_test, y_test,
                                                test_size=test_ratio / (test_ratio + validation_ratio),
                                                random_state=32)

print("Define XGBRegressor")

params = {
    'min_split_loss': 0,
    'learning_rate': 0.01,
    'max_depth': 10,
    'min_child_weight': 1,
    'subsample': 0.7059719473304258,
    'colsample_bytree': 0.8994514591758284,
    'colsample_bylevel': 0.8904199797234215,
    'colsample_bynode': 0.8754449733223327,
    'reg_lambda': 0.016916708991554074,
    'reg_alpha': 0.0011336609763898625,
    'random_state': 32,
    'objective': 'reg:squarederror',
    'tree_method': 'hist',
    'device': 'cuda',
    'sampling_method': 'gradient_based'
}

dtrain = xgb.DMatrix(x_train, y_train)
d_val = xgb.DMatrix(x_val, y_val)

# Input optimal parameters from search
# verbose_eval can crash JupyterLab - verbose_eval=False
regressor = xgb.train(params=params, dtrain=dtrain, num_boost_round=20000, early_stopping_rounds=10,
                      evals=[(dtrain, "train"), (d_val, "val")])

print("Save Model")
print(regressor.best_iteration)
regressor.save_model("D:/Wildfire_Results_v8/xgb_wildfire.json")

predictions = regressor.predict(d_val)

# Calculate MSE
mse = mean_squared_error(y_val, predictions)
print('Mean Squared Error: ', mse)

# Val %VE (Should be same as r2)
VEV = (1 - (mse / (y_val.var()))) * 100
print('%VE: ', VEV)

# Calculate RMSE
rmse = sqrt(mse)
print('Root Mean Squared Error: ', rmse)

# Val %RMSE
P_RMSE = (abs(rmse / (y_val.mean())) * 100)
print('% RMSE: ', P_RMSE)
"""
print("Run Explainer")
shap_values = regressor.predict(d_val, pred_contribs=True)

print("Format SHAP Values")
exp = shap.Explanation(shap_values[:, :-1], data=x_val, feature_names=x_val.columns)
exp_values = exp.values
print("Save SHAP Values")

# Export values to investigate
explain_export = pd.DataFrame({
    'row_id': x_val.index.values.repeat(x_val.shape[1]),
    'feature': x_val.columns.to_list() * x_val.shape[0],
    'feature_value': x_val.values.flatten(),
    'shap_values': exp_values.flatten()
})
explain_export.to_csv("D:/Wildfire_Datasets_v8/gpu_shap_df_lc.csv")
"""