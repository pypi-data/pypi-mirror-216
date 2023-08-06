# imports
import feather
import pandas
from sklearn.metrics import mean_squared_error

# + tags=["parameters"]
upstream = None
product = None
# -

# format variable
upstream = dict(upstream)

# load data from upstream
y_test = feather.read_dataframe(upstream['split_data']['test_y_data'])
del upstream['split_data']
predictions = {}
for model_name, p in upstream.items():
    predictions[model_name] = feather.read_dataframe(p['predictions'])

# + papermill={"duration": 0.011862, "end_time": "2023-06-22T11:34:46.373683", "exception": false, "start_time": "2023-06-22T11:34:46.361821", "status": "completed"}
# error
error_df = pandas.DataFrame()
# mse
for model, preds in predictions.items():
    error_df.loc[model, 'MSE'] = mean_squared_error(y_test, preds)

error_df