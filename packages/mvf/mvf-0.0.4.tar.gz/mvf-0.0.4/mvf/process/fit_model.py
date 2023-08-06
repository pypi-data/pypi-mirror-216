# imports
import feather
import pandas


def fit_py(product, upstream, model_name, split_type, n_folds=10):
    # imports
    import models

    if split_type == 'train_test':
        fit_py_train_test(
            product,
            upstream,
            model_name,
            models
        )
    elif split_type == 'k_fold':
        fit_py_k_fold(
            product,
            upstream,
            model_name,
            models,
            n_folds
        )


def fit_py_train_test(product, upstream, model_name, models):
    # load data from upstream process
    X_train = feather.read_dataframe(upstream['split_data']['train_X_data'])
    y_train = feather.read_dataframe(upstream['split_data']['train_y_data'])

    fit_model_py(
        models,
        model_name,
        X_train,
        y_train,
        product['model']
    )


def fit_py_k_fold(product, upstream, model_name, models, n_folds=10):
    # allocate memory
    X_data = []
    y_data = []
    for i in range(1, n_folds+1):
        # load data from upstream process
        X_data.append(
            feather.read_dataframe(
                upstream['split_data'][f'fold_{i}_X_data']
            )
        )
        y_data.append(
            feather.read_dataframe(
                upstream['split_data'][f'fold_{i}_y_data']
            )
        )

    # fit models
    for i in range(1, n_folds+1):
        # get train set as all folds except i-th
        X_train = pandas.concat([x for j, x in enumerate(X_data) if j != i-1])
        y_train = pandas.concat([y for j, y in enumerate(y_data) if j != i-1])

        fit_model_py(
            models,
            model_name,
            X_train,
            y_train,
            product[f'model_{i}']
        )


def fit_model_py(models, model_name, X_train, y_train, path):
    # initialise model
    model_class = getattr(models, model_name)
    model = model_class()

    # fit model
    model.fit(X_train, y_train)

    # save model for next process
    model.save(path)


def fit_r(product, upstream, model_name, split_type, n_folds=10):
    # imports
    import rpy2.robjects as robjects
    from rpy2.robjects import pandas2ri

    r = robjects.r
    r.source('models.R')

    if split_type == 'train_test':
        fit_r_train_test(
            product,
            upstream,
            model_name,
            r,
            pandas2ri
        )
    elif split_type == 'k_fold':
        fit_r_k_fold(
            product,
            upstream,
            model_name,
            r,
            pandas2ri,
            n_folds
        )


def fit_r_train_test(product, upstream, model_name, r, pandas2ri):
    # load data from upstream process
    pandas2ri.activate()
    X_train = pandas2ri.py2rpy_pandasdataframe(
        feather.read_dataframe(
            upstream['split_data']['train_X_data']
        )
    )
    y_train = pandas2ri.py2rpy_pandasdataframe(
        feather.read_dataframe(
            upstream['split_data']['train_y_data']
        )
    )
    pandas2ri.deactivate()

    # fit model and save model
    fit_model_r(
        r,
        model_name,
        X_train,
        y_train,
        str(product['model'])
    )


def fit_r_k_fold(product, upstream, model_name, r, pandas2ri, n_folds):
    # allocate memory
    X_data = []
    y_data = []
    for i in range(1, n_folds+1):
        # load data from upstream process
        X_data.append(
            feather.read_dataframe(
                upstream['split_data'][f'fold_{i}_X_data']
            )
        )
        y_data.append(
            feather.read_dataframe(
                upstream['split_data'][f'fold_{i}_y_data']
            )
        )

    # fit models
    for i in range(1, n_folds+1):
        # get train set as all folds except i-th
        pandas2ri.activate()
        X_train = pandas2ri.py2rpy_pandasdataframe(
            pandas.concat(
                [x for j, x in enumerate(X_data) if j != i-1]
            )
        )
        y_train = pandas2ri.py2rpy_pandasdataframe(
            pandas.concat(
                [y for j, y in enumerate(y_data) if j != i-1]
            )
        )
        pandas2ri.deactivate()

        fit_model_r(
            r,
            model_name,
            X_train,
            y_train,
            str(product[f'model_{i}'])
        )


def fit_model_r(r, model_name, X_train, y_train, path):
    import rpy2_r6.r6b as r6b
    # initialise model
    model_class = r6b.R6DynamicClassGenerator(r[model_name])
    model = model_class.new()

    # fit model
    model.fit(X_train, y_train)

    # save model for next process
    model.save(path)
