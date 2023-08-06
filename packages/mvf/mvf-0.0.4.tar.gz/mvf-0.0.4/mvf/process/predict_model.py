# imports
import feather
import pandas


def predict_py(upstream, product, model_name, split_type, n_folds=10):
    # format variable
    upstream = dict(upstream)

    # imports
    import models

    if split_type == 'train_test':
        # load data from upstream process
        X_test = feather.read_dataframe(upstream['split_data']['test_X_data'])
        del upstream['split_data']

        # load model from upstream process
        model_class = getattr(models, model_name)
        model = model_class()
        model.load(next(iter(upstream.values()))['model'])

        # predict
        preds = model.predict(X_test)

        # save data for next process
        feather.write_dataframe(preds, product['predictions'])
    elif split_type == 'k_fold':
        predictions = []
        for i in range(1, n_folds+1):
            # load data from upstream process
            X_test = feather.read_dataframe(
                upstream['split_data'][f'fold_{i}_X_data'])

            # load model from upstream process
            model_class = getattr(models, model_name)
            model = model_class()
            model.load(upstream[f'{model_name}_fit'][f'model_{i}'])

            # predict
            preds = model.predict(X_test)
            predictions.append(preds)
        # save data for next process
        feather.write_dataframe(
            pandas.concat(predictions),
            product['predictions']
        )


def predict_r(upstream, product, model_name, split_type, n_folds=10):
    # format variable
    upstream = dict(upstream)

    # imports
    import rpy2.robjects as robjects
    from rpy2.robjects import pandas2ri
    import rpy2_r6.r6b as r6b
    r = robjects.r
    r['source']('models.R')

    if split_type == 'train_test':
        # load data from upstream process
        pandas2ri.activate()
        X_test = pandas2ri.py2rpy_pandasdataframe(
            feather.read_dataframe(
                upstream['split_data']['test_X_data']
            )
        )
        pandas2ri.deactivate()
        del upstream['split_data']

        # load model from upstream process
        model_class = r6b.R6DynamicClassGenerator(r[model_name])
        model = model_class.new()
        model.load(str(next(iter(upstream.values()))['model']))

        # predict
        preds = model.predict(X_test)
        # convert to pandas DF
        pandas2ri.activate()
        preds = robjects.conversion.rpy2py(preds)
        pandas2ri.deactivate()

        # save data for next process
        feather.write_dataframe(preds, product['predictions'])
    elif split_type == 'k_fold':
        predictions = []
        for i in range(1, n_folds+1):
            # load data from upstream process
            pandas2ri.activate()
            X_test = pandas2ri.py2rpy_pandasdataframe(
                feather.read_dataframe(
                    upstream['split_data'][f'fold_{i}_X_data']
                )
            )
            pandas2ri.deactivate()

            # load model from upstream process
            model_class = r6b.R6DynamicClassGenerator(r[model_name])
            model = model_class.new()
            model.load(str(upstream[f'{model_name}_fit'][f'model_{i}']))

            # predict
            preds = model.predict(X_test)
            # convert to pandas DF
            pandas2ri.activate()
            preds = robjects.conversion.rpy2py(preds)
            pandas2ri.deactivate()
            predictions.append(preds)
        # save data for next process
        feather.write_dataframe(
            pandas.concat(predictions),
            product['predictions']
        )
