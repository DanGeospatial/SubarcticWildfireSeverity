"""
Optimize XGBoost with Ray Tune and HyperOPT

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
import ray
import pandas as pd
import numpy as np
from ray import tune
from ray.tune.search.hyperopt import HyperOptSearch
from sklearn.metrics import root_mean_squared_error
from xgboost import train, DMatrix
from sklearn.model_selection import train_test_split

# Import Data
checked_059 = "wildfire_dataset.csv"

train_ratio = 0.60
validation_ratio = 0.20
test_ratio = 0.20

# Preprocess Data
df = pd.read_csv(checked_059)

y = df["dNBR"]
x = df[["pre", "LC", "46_clm", "tpi", "43_clm", "35_clm", "45_clm", "VS", "WE", "23_clm", "49_clm",
        "Aspect", "33_clm", "38_clm", "50_clm", "7_clm", "42_clm", "DAH"]]

ray.init(include_dashboard=False)

# train is now 60% of the entire data set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1 - train_ratio, random_state=32)

# test is now 20% of the initial data set
# validation is now 20% of the initial data set
x_val, x_test, y_val, y_test = train_test_split(x_test, y_test,
                                                test_size=test_ratio / (test_ratio + validation_ratio), random_state=32)

# get training to ray dataframe
train_x = ray.data.from_pandas(pd.DataFrame(x_train))
train_y = ray.data.from_pandas(pd.DataFrame(y_train))

# get testing to ray dataframe
test_x = ray.data.from_pandas(pd.DataFrame(x_test))
test_y = ray.data.from_pandas(pd.DataFrame(y_test))


def objective(config):
    data_x = train_x.to_pandas()
    data_y = train_y.to_pandas()

    test_data_x = test_x.to_pandas()
    test_data_y = test_y.to_pandas()

    # Define our objective function. Here it is XGB
    params = {
        'min_split_loss': config["gamma"],
        'learning_rate': 0.01,
        'max_depth': 10,
        'min_child_weight': config["min_child_weight"],
        'subsample': config["subsample"],
        'colsample_bytree': config["colsample_bytree"],
        'colsample_bylevel': config["colsample_bylevel"],
        'colsample_bynode': config["colsample_bynode"],
        'reg_lambda': config["lambda"],
        'reg_alpha': config["alpha"],
        'random_state': 32,
        'objective': 'reg:squarederror'
    }

    dtrain = DMatrix(data_x, label=data_y)
    d_val = DMatrix(test_data_x, label=test_data_y)
    # Input optimal parameters from search
    trainer = train(params=params, dtrain=dtrain, num_boost_round=20000, early_stopping_rounds=10,
                    evals=[(dtrain, "train"), (d_val, "val")], verbose_eval=False)

    # Calculate RMSE on test split
    predictions = trainer.predict(d_val)
    rmse = root_mean_squared_error(test_data_y, predictions)

    return {"rmse": rmse}


# After running an initial tune I have an idea of what parameters are close to optimal
# If I want to check other parameter ranges I will start here
#     "max_depth": 10,
parameter_suggestion = [{
    "gamma": 2,
    "min_child_weight": 3,
    "subsample": 0.8500519790106257,
    "colsample_bytree": 0.799344898090215,
    "colsample_bylevel": 0.5579233639414936,
    "colsample_bynode": 0.7250746383986733,
    "lambda": 0.011900794313657034,
    "alpha": 0.05742342812435434
}]

# Set samples to at least 1000 for initial and 500 for refinement
method = HyperOptSearch(random_state_seed=32, points_to_evaluate=parameter_suggestion)
samples = 500

# Learning rate and n_estimators separately
# "max_depth": tune.randint(4, 11),
search_config = {
    "gamma": tune.randint(0, 4),
    "min_child_weight": tune.randint(1, 5),
    "subsample": tune.loguniform(0.5, 0.9),
    "colsample_bytree": tune.loguniform(0.2, 0.9),
    "colsample_bylevel": tune.loguniform(0.2, 0.9),
    "colsample_bynode": tune.loguniform(0.2, 0.9),
    "lambda": tune.loguniform(0.001, 3),
    "alpha": tune.loguniform(0.001, 3)
}

# Fix for trial name length issue
def trial_str_creator(trial):
    return trial.trial_id

# Currently set to cpu only
# You must compile xgboost from source on arm yourself to get gpu on the GH200
# If you have correct xgboost for arm gpu then you can modify to add gpu in tune.with_resources
trainable_with_cpu = tune.with_resources(objective, {"cpu": 15})

# Define the tuner
tuner = tune.Tuner(
    trainable_with_cpu,
    tune_config=tune.TuneConfig(
        metric="rmse",
        mode="min",
        search_alg=method,
        num_samples=samples,
        trial_dirname_creator=trial_str_creator
    ),
    param_space=search_config,
)

# Run the tunner and get optimal hyperparameters
results = tuner.fit()
print("Optimal hyperparameters: ", results.get_best_result().config)
print(results.get_best_result())
