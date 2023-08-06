import feather

def preprocess_data(product: dict):
    X = feather.read_dataframe(product['X_data'])
    y = feather.read_dataframe(product['y_data'])
    assert len(X.shape) == 2, f'Expected the X data to have 2 dimensions, has {len(X.shape)}'
    assert len(y.shape) == 2, f'Expected the y data to have 2 dimensions, has {len(y.shape)}'  
