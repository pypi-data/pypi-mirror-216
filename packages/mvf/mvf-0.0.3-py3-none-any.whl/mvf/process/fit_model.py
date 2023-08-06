# imports
import feather


def fit_py(product, upstream, model_name, split_type):
    # imports
    import models
    import pickle

    # load data from upstream process
    X_train = feather.read_dataframe(upstream['split_data']['train_X_data'])
    y_train = feather.read_dataframe(upstream['split_data']['train_y_data'])

    # initialise model
    model_class = getattr(models, model_name)
    model = model_class()

    # fit model
    model.fit(X_train, y_train)

    # save model for next process
    with open(product['model'], 'wb') as f:
        pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)


def fit_r(product, upstream, model_name, split_type):
    # imports
    import rpy2.robjects as robjects
    from rpy2.robjects import pandas2ri
    import rpy2_r6.r6b as r6b
    r = robjects.r
    r.source('models.R')

    # load data from upstream process
    pandas2ri.activate()
    X_train = pandas2ri.py2rpy_pandasdataframe(feather.read_dataframe(upstream['split_data']['train_X_data']))
    y_train = pandas2ri.py2rpy_pandasdataframe(feather.read_dataframe(upstream['split_data']['train_y_data']))
    pandas2ri.deactivate()

    # initialise model
    model_class = r6b.R6DynamicClassGenerator(r[model_name])
    model = model_class.new()

     # fit model
    model.fit(X_train, y_train)

    # save model for next process
    model.save(str(product['model']))