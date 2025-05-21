"""
Inference SHAP values from pre-trained model

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
import xgboost as xgb
import pandas as pd
import shap


v3_059 = "wildfire_dataset.csv"

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

print("Create Matrix")
d_val_sample = xgb.DMatrix(x_val, y_val)

print("Load Model")
bst = xgb.Booster(model_file="xgb_wildfire.json")

print("Run Explainer")
bst.set_param({'device': 'cuda'})
shap_values = bst.predict(d_val_sample, pred_contribs=True)

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
explain_export.to_csv("gpu_shap_df_lc.csv")
