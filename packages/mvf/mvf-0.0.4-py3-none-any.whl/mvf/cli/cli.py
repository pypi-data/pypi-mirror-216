import click
import os
import sys
from mvf.cli import cli
from mvf.cli import utils
from mvf.dag.builder import DagBuilder


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
    config = utils.load_config(os.path.join(os.getcwd(), 'mvf_conf.yaml'))
    # build dag from config
    dag_builder = DagBuilder(config, output_dir='output')
    dag_builder.build()
    click.echo('Running MVF project...')
    # access the built dag and execute it
    dag_builder.dag.build()


def plot():
    # load project config
    config = utils.load_config(os.path.join(os.getcwd(), 'mvf_conf.yaml'))
    # build dag from config
    dag_builder = DagBuilder(config, output_dir='output')
    dag_builder.build()
    click.echo('Plotting workflow...')
    # access the built dag and plot it
    dag_builder.dag.plot(os.path.join('output', 'pipeline.html'))