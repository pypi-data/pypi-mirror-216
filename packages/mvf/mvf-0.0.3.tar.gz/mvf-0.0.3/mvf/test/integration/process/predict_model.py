import feather

def predict_model(product: dict, task):
    with open(task.upstream["split_data"].product["test_y_data"], 'rb') as f:
        test_y_data = feather.read_dataframe(f)
    target_shape = test_y_data.shape
    predictions = feather.read_dataframe(product['predictions'])

    assert target_shape == predictions.shape, f'The predictions should have that same shape as the test data. Currently {predictions.shape} and {target_shape}.'
