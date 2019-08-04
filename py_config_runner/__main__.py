
import click

from py_config_runner.runner import run_script


@click.command()
@click.argument('script_filepath', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('config_filepath', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--local_rank', type=int, help="Local process rank for distributed computations")
def command(script_filepath, config_filepath, local_rank=0):
    """Method to run experiment (defined by a script file)

    Args:
        script_filepath (str): input script filepath
        config_filepath (str): input configuration filepath
        local_rank (int): local process rank for distributed computations.
            See https://pytorch.org/docs/stable/distributed.html#launch-utility
    """
    run_script(script_filepath, config_filepath, local_rank)


if __name__ == "__main__":
    command()
