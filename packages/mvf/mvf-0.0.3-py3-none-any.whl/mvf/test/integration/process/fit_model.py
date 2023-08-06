import pickle
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import rpy2_r6.r6b as r6b

def fit_model_py(product: dict, params: dict) -> None:
    # load model(s)
    with open(product['model'], 'rb') as f:
        model = pickle.load(f)
    # different tests by split type
    if params['split_type'] == 'train_test':
        # check the model has a predict method
        assert hasattr(model, 'predict'), f'The model saved at {product["model"]} must have a predict() method.'
    elif params['split_type'] == 'k_fold':
        raise NotImplementedError(f"The {params['split_type']} implementation is not tested. This is unacceptable.")
    else:
        raise NotImplementedError(f"The {params['split_type']} implementation is not tested. This is unacceptable.")

def fit_model_r(product: dict, params: dict) -> None:
    # load model
    r = robjects.r
    r.source('models.R')
    model_class = r6b.R6DynamicClassGenerator(r[params['model_name']])
    model = model_class.new()
    assert hasattr(model, 'predict'), f'The class {params["model_name"]} must have a predict() method. The class does not currently have a predict attribute.'
    assert callable(getattr(model, 'predict')), f'The class {params["model_name"]} must have a predict() method. The class\' predict attribute is not currently callable.'





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

