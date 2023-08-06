# imports
import feather
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import rpy2_r6.r6b as r6b
r = robjects.r
r['source']('models.R')

# + tags=["parameters"]
upstream = None
product = None
model_name = ''
split_type = ''
# -

# load model class
model_class = r6b.R6DynamicClassGenerator(r[model_name])

# run validation
if split_type == 'train_test':
    model = model_class.new()
    model.load(str(next(iter(upstream.values()))['model']))
    model.validate()
elif split_type == 'k_fold':
    for i in range(1, n_folds+1):
        model = model_class.new()
        model.load(str(next(iter(upstream.values()))[f'model_{i}']))
        model.validate()