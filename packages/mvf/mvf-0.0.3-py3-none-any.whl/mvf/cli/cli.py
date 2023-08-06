import click
import os
import yaml
import sys
from mvf.cli import cli
from mvf.dag.builder import build_dag
from mvf.test.integration.config import mvf as mvf_config


def cmd_router():
    '''
    CLI entry point.
    '''
    # parse the command
    cmd_name = None if len(sys.argv) <= 1 else sys.argv[1]

    # routing dict
    cmds = {
        'run': cli.run, 
        'plot': cli.plot,
    }
    if cmd_name in cmds:
        # add working dir to PYTHONPATH to allow import of local modules
        sys.path.append(os.getcwd())
        # execute command
        cmds[cmd_name]()
    else:
        raise NotImplementedError('Need an error message with hints')


### CLI COMMANDS ###


def run():
    # load project config
    config = load_config(os.path.join(os.getcwd(), 'mvf_conf.yaml'))
    dag = build_dag(config)
    click.echo('Running MVF project...')
    dag.build()


def plot():
    # load project config
    config = load_config(os.path.join(os.getcwd(), 'mvf_conf.yaml'))
    dag = build_dag(config)
    click.echo('Plotting workflow...')
    dag.plot(os.path.join('output', 'pipeline.html'))


### UTILITY FUNCTIONS


def load_config(path):
    # open the mvf config file
    try:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        raise Exception('No `mvf_conf.yaml` found in the working directory.')
    else:
        # validate the config against the schema
        click.echo('Validating config...')
        mvf_config.check_config(config)
        return config
