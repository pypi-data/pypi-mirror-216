import click
import inspect
import mvf.test.integration.config as on_render
import mvf.test.integration.process as on_finish
import mvf.process as process
import os
from pathlib import Path
from ploomber import DAG
from ploomber.products import File
from ploomber.tasks import PythonCallable, NotebookRunner


def build_dag(config):
    '''
    Builds ploomber DAG from config file.
    '''
    click.echo('Building project workflow...')
    dag = DAG(
        # set dag name as basename of working dir
        name=os.path.basename(os.getcwd())
    )

    # preprocess task
    # define task
    preprocess_data = NotebookRunner(
        source=Path(
            os.path.abspath(
                config['data']['source']
            )
        ),
        product={
            'nb': File(
                os.path.join(
                    'output', 
                    config['data']['source']
                ),
            ),
            'X_data': File(
                os.path.join(
                    'output', 
                    'preprocess_X_data.feather'
                ),
            ),
            'y_data': File(
                os.path.join(
                    'output', 
                    'preprocess_y_data.feather'
                ),
            ),
        },
        dag=dag,
        name='preprocess_data',
    )
    # hooks
    preprocess_data.on_render = on_render.preprocess_data.preprocess_data
    preprocess_data.on_finish = on_finish.preprocess_data.preprocess_data

    # split task
    # params
    params = {
        'split_type': config['data']['split']
    }
    if config['data']['split'] == 'train_test':
        params['test_size'] = config['data']['test_size']
    else:
        params['n_folds'] = config['data']['n_folds']
    # define task
    split_data = PythonCallable(
        source=process.split_data.split_data,
        product={
            'train_X_data': File(
                os.path.join(
                    'output', 
                    'train_X_data.feather'
                ),
            ),
            'test_X_data': File(
                os.path.join(
                    'output', 
                    'test_X_data.feather'
                ),
            ),
            'train_y_data': File(
                os.path.join(
                    'output', 
                    'train_y_data.feather'
                ),
            ),
            'test_y_data': File(
                os.path.join(
                    'output', 
                    'test_y_data.feather'
                ),
            ),
        },
        dag=dag,
        name='split_data',
        params=params,
    )
    # hooks
    split_data.on_render = on_render.split_data.split_data
    split_data.on_finish = on_finish.split_data.split_data
    # set upstream
    preprocess_data >> split_data

    ### validate task ###
    # path to source
    path_to_process = process.__path__[0]
    source_path = Path(
        os.path.join(
            path_to_process,
            'validate.py'
        )
    )
    # define task
    validate = NotebookRunner(
        source=source_path,
        product={
            'nb': File(
                os.path.join(
                    'output', 
                    'validate.ipynb'
                ),
            ),
        },
        dag=dag,
        name='validate',
    )
    # hooks
    validate.on_render = on_render.validate.validate
    validate.on_finish = on_finish.validate.validate
    # set upstream
    split_data >> validate
    
    # model tasks
    for model in config['models']:
        ### fit tasks ###
        model_name = model['name']
        task_name = model_name + '_fit'
        # source
        if model['lang'] == 'Python':
            source = process.fit_model.fit_py
        else:
            source = process.fit_model.fit_r
        # params
        params = {
            'model_name': model_name,
            'split_type': config['data']['split']
        }
        # define task
        fit_model = PythonCallable(
            source=source,
            product={
                'model': File(
                    os.path.join(
                        'output', 
                        task_name
                    ),
                ),
            },
            dag=dag,
            name=task_name,
            params=params,
        )
        # hooks
        if model['lang'] == 'Python':
            fit_model.on_render = on_render.fit_model.fit_model_py
            fit_model.on_finish = on_finish.fit_model.fit_model_py
        else:
            fit_model.on_render = on_render.fit_model.fit_model_r
            fit_model.on_finish = on_finish.fit_model.fit_model_r
        # set upstream
        split_data >> fit_model

        ### validate tasks ###
        if model['validation_step']:
            task_name = model_name + '_validate'
            # source
            if model['lang'] == 'Python':
                source_path = Path(
                    os.path.join(
                        path_to_process,
                        'validate_model_py.py'
                    )
                )
            else:
                source_path = Path(
                    os.path.join(
                        path_to_process,
                        'validate_model_r.py'
                    )
                )
            # define task
            validate_model = NotebookRunner(
                source=source_path,
                product={
                    'nb': File(
                        os.path.join(
                            'output', 
                            task_name + '.html'
                        ),
                    ),
                },
                dag=dag,
                name=task_name,
                params = {
                    'model_name': model_name,
                },
            )
            # hooks
            validate_model.on_render = on_render.validate_model.validate_model
            validate_model.on_finish = on_finish.validate_model.validate_model
            # set upstream
            fit_model >> validate_model
        else:
            pass

        ### predict task ###
        task_name = model_name + '_predict'
        # source
        if model['lang'] == 'Python':
            source = process.predict_model.predict_py
        else:
            source = process.predict_model.predict_r
        # define task
        predict_model = PythonCallable(
            source=source,
            product={
                'predictions': File(
                    os.path.join(
                        'output', 
                        task_name + '.feather'
                    ),
                ),
            },
            dag=dag,
            name=task_name,
            params = {
                'model_name': model_name,
            }
        )
        # hooks  
        predict_model.on_render = on_render.predict_model.predict_model
        predict_model.on_finish = on_finish.predict_model.predict_model
        # set upstream
        split_data >> predict_model
        fit_model >> predict_model
        predict_model >> validate

    return dag