from schema import Schema, Or, Optional, And


def check_config(config):
    # schema for mvf_conf.yaml
    mvf_conf = Schema(
        {
            'project_name': str,
            'data': {
                'source': str,
                'split': Or('train_test', 'k_fold'),
                Optional('test_size'): lambda x: 0 <= x <= 1,
                Optional('n_folds'): And(int, lambda x: x > 0),
            },
            'models': [
                {
                    'name': str,
                    'lang': Or('Python', 'R'),
                    'validation_step': bool,
                }
            ],
        }
    )
    # validate given schema
    mvf_conf.validate(config)
    # additional validation
    if 'n_folds' in config['data'] and 'test_size' in config['data']:
        raise Exception('Only one of `test_size` and `n_folds` may be specified.')
    if config['data']['split'] == 'train_test' and 'n_folds' in config['data']:
        raise Exception('`n_folds` is not a valid parameter for a \'train_test\' split.')
    if config['data']['split'] == 'k_fold' and 'test_size' in config['data']:
        raise Exception('`test_size` is not a valid parameter for a \'k_fold\' split.')
