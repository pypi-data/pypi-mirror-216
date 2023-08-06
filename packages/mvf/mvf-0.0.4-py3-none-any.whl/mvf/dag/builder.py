import click
import mvf.integration.config as on_render
import mvf.integration.process as on_finish
import mvf.process as process
import os
from pathlib import Path
from ploomber import DAG
from ploomber.products import File
from ploomber.tasks import PythonCallable, NotebookRunner


class DagBuilder:
    def __init__(self, config, output_dir='output') -> None:
        '''
        Assigns key parameters as attributes. Initialises the Ploomber DAG.
        '''
        click.echo('Building project workflow...')
        self.config = config
        self.output_dir = output_dir
        # path to source code
        self.path_to_process = process.__path__[0]
        self.dag = DAG(
            # set dag name as basename of working dir
            name=os.path.basename(os.getcwd())
        )


    def build(self):
        '''
        Main method for the class.

        Builds ploomber DAG from config file.
        '''
        # build up generic tasks
        preprocess_data = self.__build_preprocess_data()
        split_data = self.__build_split_data()
        validate = self.__build_validate()
        # model tasks
        for model in self.config['models']:
            # get model params
            name = model['name']
            lang = model['lang']
            val_step = model['validation_step']
            # build up model tasks
            fit_model = self.__build_fit_model(name, lang)
            predict_model = self.__build_predict_model(name, lang)
            if val_step:
                validate_model = self.__build_validate_model(name, lang)
                # set upstream
                fit_model >> validate_model
            # set upstream
            split_data >> fit_model
            split_data >> predict_model
            fit_model >> predict_model
            predict_model >> validate
        # set upstream
        preprocess_data >> split_data
        split_data >> validate


    def __build_preprocess_data(self):
        # define task
        preprocess_data = NotebookRunner(
            source=Path(
                os.path.abspath(
                    self.config['data']['source']
                )
            ),
            product={
                'nb': File(
                    os.path.join(
                        self.output_dir,
                        'notebooks',
                        self.config['data']['source']
                    ),
                ),
                'X_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'preprocess_X_data.feather'
                    ),
                ),
                'y_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'preprocess_y_data.feather'
                    ),
                ),
            },
            dag=self.dag,
            name='preprocess_data',
        )
        # hooks
        preprocess_data.on_render = on_render.preprocess_data.preprocess_data
        preprocess_data.on_finish = on_finish.preprocess_data.preprocess_data
        return preprocess_data


    def __build_split_data(self):
        # params
        params = {
            'split_type': self.config['data']['split']
        }
        # define params based on split_type
        if self.config['data']['split'] == 'train_test':
            params['test_size'] = self.config['data']['test_size']
            product = {
                'train_X_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'train_X_data.feather'
                    ),
                ),
                'test_X_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'test_X_data.feather'
                    ),
                ),
                'train_y_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'train_y_data.feather'
                    ),
                ),
                'test_y_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'test_y_data.feather'
                    ),
                ),
            }
        else:
            n_folds = self.config['data']['n_folds']
            params['n_folds'] = n_folds
            product = {
                f'fold_{i}_X_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        f'fold_{i}_X_data.feather'
                    ),
                )
                for i in range(1, n_folds + 1)
            }
            product_y = {
                f'fold_{i}_y_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        f'fold_{i}_y_data.feather'
                    ),
                )
                for i in range(1, n_folds + 1)
            }
            product.update(product_y)
        # define task
        split_data = PythonCallable(
            source=process.split_data.split_data,
            product=product,
            dag=self.dag,
            name='split_data',
            params=params,
        )
        # hooks
        split_data.on_render = on_render.split_data.split_data
        split_data.on_finish = on_finish.split_data.split_data
        return split_data
    

    def __build_fit_model(self, name, lang):
        task_name = name + '_fit'
        # source
        if lang == 'Python':
            source = process.fit_model.fit_py
        else:
            source = process.fit_model.fit_r
        # params
        params = {
            'model_name': name,
            'split_type': self.config['data']['split']
        }
        if self.config['data']['split'] == 'k_fold':
            params['split_type'] = self.config['data']['split']
            params['n_folds'] = self.config['data']['n_folds']
            product = {
                f'model_{i}': File(
                    os.path.join(
                        self.output_dir,
                        'models',
                        task_name + f'_{i}'
                    ),
                )
                for i in range(1, self.config['data']['n_folds'] + 1)
            }
        else:
            product = {
                'model': File(
                    os.path.join(
                        self.output_dir,
                        'models',
                        task_name
                    ),
                ),
            }
        # define task
        fit_model = PythonCallable(
            source=source,
            product=product,
            dag=self.dag,
            name=task_name,
            params=params,
        )
        # hooks
        if lang == 'Python':
            fit_model.on_render = on_render.fit_model.fit_model_py
            fit_model.on_finish = on_finish.fit_model.fit_model_py
        else:
            fit_model.on_render = on_render.fit_model.fit_model_r
            fit_model.on_finish = on_finish.fit_model.fit_model_r
        return fit_model


    def __build_predict_model(self, name, lang):
        task_name = name + '_predict'
        # source
        if lang == 'Python':
            source = process.predict_model.predict_py
        else:
            source = process.predict_model.predict_r
        # params
        params = {
            'model_name': name,
        }
        if self.config['data']['split'] == 'k_fold':
            params['split_type'] = self.config['data']['split']
            params['n_folds'] = self.config['data']['n_folds']
        # define task
        predict_model = PythonCallable(
            source=source,
            product={
                'predictions': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        task_name + '.feather'
                    ),
                ),
            },
            dag=self.dag,
            name=task_name,
            params=params
        )
        # hooks  
        predict_model.on_render = on_render.predict_model.predict_model
        predict_model.on_finish = on_finish.predict_model.predict_model
        return predict_model
    

    def __build_validate_model(self, name, lang):
        task_name = name + '_validate'
        # source
        if lang == 'Python':
            source_path = Path(
                os.path.join(
                    self.path_to_process,
                    'validate_model_py.py'
                )
            )
        else:
            source_path = Path(
                os.path.join(
                    self.path_to_process,
                    'validate_model_r.py'
                )
            )
        # params
        params = {
            'model_name': name,
        }
        if self.config['data']['split'] == 'k_fold':
            params['split_type'] = self.config['data']['split']
            params['n_folds'] = self.config['data']['n_folds']
        # define task
        validate_model = NotebookRunner(
            source=source_path,
            product={
                'nb': File(
                    os.path.join(
                        self.output_dir,
                        'notebooks',
                        task_name + '.html'
                    ),
                ),
            },
            dag=self.dag,
            name=task_name,
            params=params,
        )
        # hooks
        validate_model.on_render = on_render.validate_model.validate_model
        validate_model.on_finish = on_finish.validate_model.validate_model
        return validate_model


    def __build_validate(self):
        source_path = Path(
            os.path.join(
                self.path_to_process,
                'validate.py'
            )
        )
        # params
        params = {
            'split_type': self.config['data']['split'],
        }
        if self.config['data']['split'] == 'k_fold':
            params['n_folds'] = self.config['data']['n_folds']
        # define task
        validate = NotebookRunner(
            source=source_path,
            product={
                'nb': File(
                    os.path.join(
                        self.output_dir,
                        'notebooks',
                        'validate.ipynb'
                    ),
                ),
                'nb_html': File(
                    os.path.join(
                        self.output_dir,
                        'notebooks',
                        'validate.html'
                    ),
                ),
            },
            nb_product_key=[
                'nb',
                'nb_html'
            ],
            dag=self.dag,
            name='validate',
            params=params,
        )
        # hooks
        validate.on_render = on_render.validate.validate
        validate.on_finish = on_finish.validate.validate
        return validate
    