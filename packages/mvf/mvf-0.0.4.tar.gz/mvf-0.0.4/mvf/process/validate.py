# imports
import feather
import pandas
from sklearn.metrics import mean_squared_error

# + tags=["parameters"]
upstream = None
product = None
split_type = ''
n_folds = 10
# -

# format variable
upstream = dict(upstream)

# load ground truth data from upstream
if split_type == 'train_test':
    ground_truth = feather.read_dataframe(upstream['split_data']['test_y_data'])
elif split_type == 'k_fold':
    ground_truth = []
    for i in range(1, n_folds+1):   
        ground_truth.append(
            feather.read_dataframe(upstream['split_data'][f'fold_{i}_y_data'])
        )
    ground_truth = pandas.concat(ground_truth)
del upstream['split_data']

# load predictions from upstream
predictions = {}
for model_name, p in upstream.items():
    predictions[model_name] = feather.read_dataframe(p['predictions'])

# + papermill={"duration": 0.011862, "end_time": "2023-06-22T11:34:46.373683", "exception": false, "start_time": "2023-06-22T11:34:46.361821", "status": "completed"}
# error
error_df = pandas.DataFrame()
# mse
for model, preds in predictions.items():
    error_df.loc[model, 'MSE'] = mean_squared_error(ground_truth, preds)

error_df