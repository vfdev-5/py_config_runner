
import click

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


@click.command()
@click.argument('script_filepath', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('config_filepath', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--manual_config_load', is_flag=True, help="Allow manual configuration file loading")
@click.option('--local_rank', type=int, default=0, help="Local process rank for distributed computations")
def command(script_filepath, config_filepath, manual_config_load, local_rank):
    """Method to run experiment (defined by a script file)

    Args:
        script_filepath (str): input script filepath
        config_filepath (str): input configuration filepath
        manual_config_load (bool): if True configuration file can be manually loaded using
            `py_config_runner.runner.setup_config` method.
        local_rank (int): local process rank for distributed computations.
            See https://pytorch.org/docs/stable/distributed.html#launch-utility
    """

    # remove path to py_config_runner.py_config_runner module from sys.path
    # as it can interfere with user's modules: py_config_runner.utils (seen as utils) <--> utils.py (user's module)
    this_folder_path = Path(__file__).parent.as_posix()
    import sys
    if this_folder_path in sys.path:
        sys.path.remove(this_folder_path)

    from py_config_runner.runner import run_script

    run_script(script_filepath, config_filepath, manual_config_load=manual_config_load, local_rank=local_rank)


def print_script_filepath():
    # This is helpful to call the runner using other executables
    # Ex1. python -m launcher `py_config_runner_script` script.py config.py
    # Ex2. python -m torch.distributed.launch `py_config_runner_script` script.py config.py
    print(__file__)


if __name__ == "__main__":
    command()
