# imports
import feather


def predict_py(upstream, product, model_name):
    # format variable
    upstream = dict(upstream)

    # imports
    import pickle
    import pandas
    
    # load data from upstream process
    X_test = feather.read_dataframe(upstream['split_data']['test_X_data'])
    del upstream['split_data']

    # load model from upstream process
    with open(next(iter(upstream.values()))['model'], 'rb') as f:
        model = pickle.load(f)

    # predict
    preds = model.predict(X_test)

    # save data for next process
    feather.write_dataframe(preds, product['predictions'])

def predict_r(upstream, product, model_name):
    # format variable
    upstream = dict(upstream)
    
    # imports
    import rpy2.robjects as robjects
    from rpy2.robjects import pandas2ri
    import rpy2_r6.r6b as r6b
    r = robjects.r
    r['source']('models.R')

    # load data from upstream process
    pandas2ri.activate()
    X_test = pandas2ri.py2rpy_pandasdataframe(feather.read_dataframe(upstream['split_data']['test_X_data']))
    pandas2ri.deactivate()
    print(type(upstream))
    print(upstream)
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