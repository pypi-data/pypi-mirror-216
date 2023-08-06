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
# -

# load model from upstream process
model_class = r6b.R6DynamicClassGenerator(r[model_name])
model = model_class.new()
model.load(str(next(iter(upstream.values()))['model']))

# run validation
model.validate()