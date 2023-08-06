import feather

def split_data(product: dict, params: dict):
    # different tests by split type
    if params['split_type'] == 'train_test':
        X_train = feather.read_dataframe(product['train_X_data'])
        X_test = feather.read_dataframe(product['test_X_data'])
        y_train = feather.read_dataframe(product['train_y_data'])
        y_test = feather.read_dataframe(product['test_y_data'])

        assert X_train.shape[0] == y_train.shape[0], f'X and y train data should have the same number of instances. Currently {X_train.shape[0]} and {y_train.shape[0]}'
        assert X_test.shape[0] == y_test.shape[0], f'X and y test data should have the same number of instances. Currently {X_test.shape[0]} and {y_test.shape[0]}'
        assert X_train.shape[1] == X_test.shape[1], f'X train and test data should have the same number of features. Currently {X_train.shape[1]} and {X_test.shape[1]}'
        assert y_train.shape[1] == y_test.shape[1], f'y train and test data should have the same number of features. Currently {y_train.shape[1]} and {y_test.shape[1]}'
        assert (X_test.shape[0] / (X_test.shape[0] + X_train.shape[0])) - params['test_size'] < 1e-4, 'The actual test size differs too much from the test_size parameter. If you have a very small dataset, choose an appropriate test size for the number of data points.'
        assert (X_train.index == y_train.index).all(), 'The indices for X and y training data do not match up.'
        assert (X_test.index == y_test.index).all(), 'The indices for X and y testing data do not match up.'
        assert len(set(X_train.index).intersection(set(X_test.index))) == 0, 'The train and test indices are not distinct.'
    elif params['split_type'] == 'k_fold':
        X_data = []
        y_data = []
        n_instances = set()
        indices = []
        for i in range(1, params['n_folds'] + 1):
            fold_i_X_data = feather.read_dataframe(product[f'fold_{i}_X_data'])
            fold_i_y_data = feather.read_dataframe(product[f'fold_{i}_y_data'])

            assert fold_i_X_data.shape[0] == fold_i_y_data.shape[0], f'X and y data from a particular fold should have the same number of instances. Currently {fold_i_X_data.shape[0]} and {fold_i_y_data.shape[0]} for the {i}th fold.'
            assert (fold_i_X_data.index == fold_i_y_data.index).all(), f'The indices for X and y from the {i}th fold do not match up.'
            
            X_data.append(fold_i_X_data)
            y_data.append(fold_i_y_data)
            n_instances.add(fold_i_X_data.shape[0])
            indices.append(set(fold_i_X_data.index))

        assert len(n_instances) <= 2 and -1 <= list(n_instances)[0] - list(n_instances)[-1] <= 1, f'The number of instances in each fold must be as equal as possible. The number of instances in folds are currently {n_instances}.'
        assert len(set.intersection(*indices)) == 0, 'The fold indices are not distinct.'

        for i in range(params['n_folds'] - 1):
            assert X_data[i].shape[1] == X_data[i+1].shape[1], f'X data should have the same number of features across all folds. {i}th fold has {X_data[i].shape[1]} features but {i+1}th fold has {X_data[i+1].shape[1]} features.'
            assert y_data[i].shape[1] == y_data[i+1].shape[1], f'y data should have the same number of features across all folds. {i}th fold has {y_data[i].shape[1]} features but {i+1}th fold has {y_data[i+1].shape[1]} features.'
    else:
        raise NotImplementedError(f"The {params['split_type']} implementation is not tested. This is unacceptable.")
