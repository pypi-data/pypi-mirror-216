import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import rpy2_r6.r6b as r6b

def fit_model_py(product: dict, params: dict) -> None:
    import models
    # get model class
    model_class = getattr(models, params['model_name'])
    # different tests by split type
    if params['split_type'] == 'train_test':
        # load model
        model = model_class()
        model.load(product['model'])
        # check the model has a predict method
        assert hasattr(model, 'predict'), f'The model saved at {product["model"]} must have a predict() method.'
        assert callable(getattr(model, 'predict')), f'The model saved at {product["model"]} must have a predict() method. The class\' predict attribute is not currently callable.'
    elif params['split_type'] == 'k_fold':
        for i in range(1, params['n_folds'] + 1):
            model = model_class()
            model.load(product[f'model_{i}'])
            # check the model has a predict method
            assert hasattr(model, 'predict'), f'The model saved at {product["model"]} must have a predict() method.'
            assert callable(getattr(model, 'predict')), f'The model saved at {product["model"]} must have a predict() method. The class\' predict attribute is not currently callable.'
    else:
        raise NotImplementedError(f"The {params['split_type']} implementation is not tested. This is unacceptable.")

def fit_model_r(product: dict, params: dict) -> None:
    # load model
    r = robjects.r
    r.source('models.R')
    model_class = r6b.R6DynamicClassGenerator(r[params['model_name']])

    # different tests by split type
    if params['split_type'] == 'train_test':
        # load model
        model = model_class.new()
        model.load(str(product['model']))
        # check the model has a predict method
        assert hasattr(model, 'predict'), f'The model saved at {product["model"]} must have a predict() method.'
        assert callable(getattr(model, 'predict')), f'The model saved at {product["model"]} must have a predict() method. The class\' predict attribute is not currently callable.'
    elif params['split_type'] == 'k_fold':
        for i in range(1, params['n_folds'] + 1):
            model = model_class.new()
            model.load(str(product[f'model_{i}']))
            # check the model has a predict method
            assert hasattr(model, 'predict'), f'The model saved at {product["model"]} must have a predict() method.'
            assert callable(getattr(model, 'predict')), f'The model saved at {product["model"]} must have a predict() method. The class\' predict attribute is not currently callable.'
    else:
        raise NotImplementedError(f"The {params['split_type']} implementation is not tested. This is unacceptable.")
    



#### example code for debugging a test
# ensure correct data is in locations specified
# run test using
#
#   python3 fit_model.py

# from ploomber.products import File

# if __name__ == '__main__':
#     product = {
#         'nb': File('/home/tom/projects/model-validation-framework/examples/project1/output/fit_model_2.ipynb'),
#         'nb_html': File('/home/tom/projects/model-validation-framework/examples/project1/output/fit_model_2.html'),
#         'model': File('/home/tom/projects/model-validation-framework/examples/project1/output/fit_model_2')
#     }
#     fit_model_r(product)

