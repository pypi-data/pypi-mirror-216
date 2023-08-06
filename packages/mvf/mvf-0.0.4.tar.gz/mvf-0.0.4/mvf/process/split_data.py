# imports
import feather
from sklearn.model_selection import train_test_split, KFold


def split_data(upstream, product, split_type, test_size=0.5, n_folds=10):
    # load data from upstream process
    X = feather.read_dataframe(upstream['preprocess_data']['X_data'])
    y = feather.read_dataframe(upstream['preprocess_data']['y_data'])

    # parse split_type parameter
    if split_type == 'train_test':
        # split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, 
            y, 
            test_size=test_size
        )
        # print metadata
        print(f'X_train shape: {X_train.shape}')
        print(f'X_test shape: {X_test.shape}')
        print(f'y_train shape: {y_train.shape}')
        print(f'y_test shape: {y_test.shape}')
        # save data for next process
        feather.write_dataframe(X_train, product['train_X_data'])
        feather.write_dataframe(X_test, product['test_X_data'])
        feather.write_dataframe(y_train, product['train_y_data'])
        feather.write_dataframe(y_test, product['test_y_data'])
    elif split_type == 'k_fold':
        kfolds = KFold(n_splits=n_folds)
        for i, (train_idx, test_idx) in enumerate(kfolds.split(X)):
            # split data
            fold_X_data = X.iloc[test_idx]
            fold_y_data = y.iloc[test_idx]
            # print metadata
            print(f'Fold {i+1} X shape: {fold_X_data.shape}')        
            print(f'Fold {i+1} y shape: {fold_y_data.shape}')
            # save data for next process   
            feather.write_dataframe(fold_X_data, product[f'fold_{i+1}_X_data'])   
            feather.write_dataframe(fold_y_data, product[f'fold_{i+1}_y_data'])   
