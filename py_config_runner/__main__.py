from pathlib import Path

import click


@click.command()
@click.argument("script_filepath", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument("config_filepath", type=click.Path(exists=True, file_okay=True, dir_okay=False))
def command(script_filepath: str, config_filepath: str) -> None:
    """Method to run experiment (defined by a script file)

    Args:
        script_filepath: input script filepath
        config_filepath: input configuration filepath
    """

    # remove path to py_config_runner.py_config_runner module from sys.path
    # as it can interfere with user's modules: py_config_runner.utils (seen as utils) <--> utils.py (user's module)
    this_folder_path = Path(__file__).parent.as_posix()
    import sys

    if this_folder_path in sys.path:
        sys.path.remove(this_folder_path)

    from py_config_runner.runner import run_script

    run_script(script_filepath, config_filepath)


def print_script_filepath() -> None:
    # This is helpful to call the runner using other executables
    # Ex1. python -m launcher `py_config_runner_script` script.py config.py
    # Ex2. python -m torch.distributed.launch `py_config_runner_script` script.py config.py
    print(__file__)


if __name__ == "__main__":
    command()
