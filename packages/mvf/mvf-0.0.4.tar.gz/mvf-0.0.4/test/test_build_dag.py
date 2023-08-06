from mvf.dag.builder import DagBuilder
from mvf.cli.utils import load_config
from ploomber.spec import DAGSpec
import os
import pytest

@pytest.mark.parametrize(
    ('test_project_path'),
    [
        ('test/test_resources/test_project_1'),
        ('test/test_resources/test_project_2')
    ]
)


def test_build_dag(test_project_path):
    '''
    Tests

        * Python `preprocess_data` template
        * `train_test` parameter on the `split_data` process
    '''
    testing_dir = os.getcwd()
    os.chdir(test_project_path)

    try:
        # load in output dag
        spec = DAGSpec('pipeline.yaml')
        expected_dag = spec.to_dag()

        # load config
        config = load_config('mvf_conf.yaml')
        # build dag from config
        dag_builder = DagBuilder(config)
        dag_builder.build()
        dag = dag_builder.dag

        ###
        ### TESTING ###
        ###
        assert dag.name == expected_dag.name

        ### preprocess task ###
        preprocess = dag.get('preprocess_data')
        expected = expected_dag.get('preprocess_data')

        # source
        assert preprocess.source.loc == expected.source.loc
        # product
        assert preprocess.product['nb'] == expected.product['nb']
        assert preprocess.product['X_data'] == expected.product['X_data']
        assert preprocess.product['y_data'] == expected.product['y_data']
        # name
        assert preprocess.name == expected.name
        # hooks
        assert preprocess.on_render.__name__ == expected.on_render.callable.__name__
        assert preprocess.on_finish.__name__ == expected.on_finish.callable.__name__

        ### split task ###
        split = dag.get('split_data')
        expected = expected_dag.get('split_data')

        # source
        assert split.source.loc == expected.source.loc
        # product
        if config['data']['split'] == 'train_test':
            assert split.product['train_X_data'] == expected.product['train_X_data']
            assert split.product['test_X_data'] == expected.product['test_X_data']
            assert split.product['train_y_data'] == expected.product['train_y_data']
            assert split.product['test_y_data'] == expected.product['test_y_data']
        elif config['data']['split'] == 'k_fold':
            n_folds = config['data']['n_folds']
            for i in range(1, n_folds + 1):
                assert split.product[f'fold_{i}_X_data'] == expected.product[f'fold_{i}_X_data']
                assert split.product[f'fold_{i}_y_data'] == expected.product[f'fold_{i}_y_data']
        # params
        assert split.params == expected.params
        # upstream
        assert split.upstream.keys() == expected.upstream.keys()
        # name
        assert split.name == expected.name
        # hooks
        assert split.on_render.__name__ == expected.on_render.callable.__name__
        assert split.on_finish.__name__ == expected.on_finish.callable.__name__

        ### model tasks ###
        for model in config['models']:
            model_name = model['name']

            ### fit task ###
            fit = dag.get(model_name + '_fit')
            expected = expected_dag.get(model_name + '_fit')

            # source
            assert fit.source.loc == expected.source.loc
            # product
            if config['data']['split'] == 'train_test':
                assert fit.product['model'] == expected.product['model']
            elif config['data']['split'] == 'k_fold':
                n_folds = config['data']['n_folds']
                for i in range(1, n_folds + 1):
                    assert fit.product[f'model_{i}'] == expected.product[f'model_{i}']
            # params
            assert fit.params == expected.params
            # upstream
            assert fit.upstream.keys() == expected.upstream.keys()
            # name
            assert fit.name == expected.name
            # hooks
            assert fit.on_render.__name__ == expected.on_render.callable.__name__
            assert fit.on_finish.__name__ == expected.on_finish.callable.__name__

            ### validate model task ###
            validate = dag.get(model_name + '_validate')
            expected = expected_dag.get(model_name + '_validate')
            if model['validation_step']:
                # source
                assert validate.source.loc.resolve() == expected.source.loc.resolve()
                # product
                assert validate.product['nb'] == expected.product['nb']
                # params
                assert validate.params == expected.params
                # upstream
                assert validate.upstream.keys() == expected.upstream.keys()
                # name
                assert validate.name == expected.name
                # hooks
                assert validate.on_render.__name__ == expected.on_render.callable.__name__
                assert validate.on_finish.__name__ == expected.on_finish.callable.__name__
            else:
                assert validate is None

            ### predict model task ###
            predict = dag.get(model_name + '_predict')
            expected = expected_dag.get(model_name + '_predict')
            # source
            assert predict.source.loc == expected.source.loc
            # product
            assert predict.product['predictions'] == expected.product['predictions']
            # upstream
            assert predict.upstream.keys() == expected.upstream.keys()
            # name
            assert predict.name == expected.name
            # hooks
            assert predict.on_render.__name__ == expected.on_render.callable.__name__
            assert predict.on_finish.__name__ == expected.on_finish.callable.__name__
            # params
            assert predict.params == expected.params
        
        ### validate task ###
        validate = dag.get('validate')
        expected = expected_dag.get('validate')

        # source
        assert validate.source.loc.resolve() == expected.source.loc.resolve()
        # product
        assert validate.product['nb'] == expected.product['nb']
        # upstream
        assert validate.upstream.keys() == expected.upstream.keys(), f'Upstream tasks are {validate.upstream.keys()}. Should be {expected.upstream.keys()}.'
        # params
        assert validate.params == expected.params
        # name
        assert validate.name == expected.name
        # hooks
        assert validate.on_render.__name__ == expected.on_render.callable.__name__
        assert validate.on_finish.__name__ == expected.on_finish.callable.__name__

    finally:
        os.chdir(testing_dir)
    
