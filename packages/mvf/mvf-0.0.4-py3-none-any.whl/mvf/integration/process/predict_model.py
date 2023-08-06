import pandas
import feather


def predict_model(product: dict, task, params):
    if params['split_type'] == 'train_test':
        with open(task.upstream['split_data'].product['test_y_data'], 'rb') as f:
            target_data = feather.read_dataframe(f)
    elif params['split_type'] == 'k_fold':
        target_data = []
        for i in range(1, params['n_folds']+1):
            with open(task.upstream['split_data'].product[f'fold_{i}_y_data'], 'rb') as f:
                target_data.append(
                    feather.read_dataframe(f)
                )
        target_data = pandas.concat(target_data)

    target_shape = target_data.shape
    predictions = feather.read_dataframe(product['predictions'])

    assert target_shape == predictions.shape, f'The predictions should have that same shape as the test data. Currently {predictions.shape} and {target_shape}.'
