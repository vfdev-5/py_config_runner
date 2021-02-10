import os
import sys
import inspect

from pathlib import Path
from typing import Any

from py_config_runner.utils import load_module, ConfigObject


def run_script(script_file: str, config_file: str, **kwargs: Any) -> None:
    """Method to run experiment (defined by a script file)

    Args:
        script_filepath (str): input script filepath
        config_filepath (str): input configuration filepath
    """
    # Add config path and current working directory to sys.path to correctly load the configuration
    script_filepath = Path(script_file)
    config_filepath = Path(config_file)
    sys.path.insert(0, script_filepath.resolve().parent.as_posix())
    sys.path.insert(0, config_filepath.resolve().parent.as_posix())
    sys.path.insert(0, os.getcwd())

    module = load_module(script_filepath)
    _check_script(module)

    run_fn = module.__dict__["run"]

    # Lazy setup configuration
    config = ConfigObject(config_filepath, script_filepath=script_filepath)

    run_fn(config, **kwargs)


def _check_script(module):
    if "run" not in module.__dict__:
        raise RuntimeError("Script file '{}' should contain a method `run(config, **kwargs)`".format(module.__file__))

    run_fn = module.__dict__["run"]

    if not callable(run_fn):
        raise RuntimeError("Run method from script file '{}' should be a callable function".format(module.__file__))

    # Check the signature
    exception_msg = None
    kwargs = {}
    config = None
    logger = None
    if sys.version_info[0] < 3:
        try:
            callable_ = run_fn if hasattr(run_fn, "__name__") else run_fn.__call__
            inspect.getcallargs(callable_, config, logger=logger, **kwargs)
        except TypeError as exc:
            exception_msg = str(exc)
    else:
        signature = inspect.signature(run_fn)
        try:
            signature.bind(config, logger=logger, **kwargs)
        except TypeError as exc:
            exception_msg = str(exc)

    if exception_msg:
        raise RuntimeError("Run method signature should be `run(config, **kwargs)`, but got {}".format(exception_msg))


if __name__ == "__main__":
    # To run profiler
    assert len(sys.argv) == 3
    run_script(sys.argv[1], sys.argv[2])
