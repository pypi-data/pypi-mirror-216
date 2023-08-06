import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import rpy2_r6.r6b as r6b


def fit_model_params(product: dict, params: dict) -> None:
    # check params for fit_model tasks
    assert 'model' in product, 'The \'model\' product must be defined.'
    assert 'model_name' in params, 'The \'model_name\' parameter must be defined.'
    assert 'split_type' in params, 'The \'split_type\' parameter must be defined.'


def fit_model_r(product: dict, params: dict) -> None:
    # check params
    fit_model_params(product, params)
    # check that the correct model class is available
    r = robjects.r
    try:
        r.source('models.R')
        model_class = r6b.R6DynamicClassGenerator(r[params["model_name"]])
        model = model_class.new()
        # check the model class has a callable 'fit' method
        assert hasattr(model, 'fit'), f'The class {params["model_name"]} must have a fit() method. The class does not currently have a fit attribute.'
        assert callable(getattr(model, 'fit')), f'The class {params["model_name"]} must have a fit() method. The class\' fit attribute is not currently callable.'
    except rpy2.rinterface_lib.embedded.RRuntimeError:
        raise ModuleNotFoundError(f'If using a R based model for {params["model_name"]}, you must have a models.R file in your project directory.')


def fit_model_py(product: dict, params: dict) -> None:
    # check params
    fit_model_params(product, params)
    # check that the correct model class is available
    try:
        import models
        assert hasattr(models, params['model_name']), f'models.py must contain a class called {params["model_name"]}.'
        model_class = getattr(models, params['model_name'])
        # check the model class has a callable 'fit' method
        assert hasattr(model_class, 'fit'), f'The class {params["model_name"]} must have a fit() method. The class does not currently have a fit attribute.'
        assert callable(getattr(model_class, 'fit')), f'The class {params["model_name"]} must have a fit() method. The class\' fit attribute is not currently callable.'
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f'If using a Python based model for {params["model_name"]}, you must have a models.py file in your project directory. The project directory is {os.getcwd()}')
    

from ploomber.products import File

if __name__ == '__main__':
    product = {
        'nb': File('/home/tom/projects/model-validation-framework/examples/project1/output/fit_model_2.ipynb'),
        'nb_html': File('/home/tom/projects/model-validation-framework/examples/project1/output/fit_model_2.html'),
        'model': File('/home/tom/projects/model-validation-framework/examples/project1/output/fit_model_2')
    }
    params = {
      'model_name': 'BayesReg',
      'split_type': 'train_test'
    }
    fit_model_r(product, params)
