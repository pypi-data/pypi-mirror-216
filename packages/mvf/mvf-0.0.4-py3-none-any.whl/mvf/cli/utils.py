import click
import yaml
from mvf.integration import mvf_config

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