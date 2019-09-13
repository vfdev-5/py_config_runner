
import os
import sys
import logging
import inspect

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


from py_config_runner.utils import load_module, setup_logger


def run_script(script_filepath, config_filepath, **kwargs):
    """Method to run experiment (defined by a script file)

    Args:
        script_filepath (str): input script filepath
        config_filepath (str): input configuration filepath
    """
    # Add config path and current working directory to sys.path to correctly load the configuration
    sys.path.insert(0, Path(script_filepath).resolve().parent.as_posix())
    sys.path.insert(0, Path(config_filepath).resolve().parent.as_posix())
    sys.path.insert(0, os.getcwd())

    module = load_module(script_filepath)
    _check_script(module)

    exp_name = module.__name__
    run_fn = module.__dict__['run']

    # Setup configuration
    if kwargs.get('manual_config_load', False):
        config = _ConfigObject(config_filepath, script_filepath)
    else:
        config = _setup_config(config_filepath, script_filepath)

    logger = logging.getLogger(exp_name)
    log_level = logging.INFO
    setup_logger(logger, log_level)

    try:
        run_fn(config, logger=logger, **kwargs)
    except KeyboardInterrupt:
        logger.info("Catched KeyboardInterrupt -> exit")
    except Exception as e:  # noqa
        logger.exception("")
        raise e


class _ConfigObject:

    def __init__(self, config_filepath, script_filepath):
        self.config_filepath = config_filepath
        self.script_filepath = script_filepath

    def setup(self):
        return _setup_config(self.config_filepath, self.script_filepath)


def _setup_config(config_filepath, script_filepath):
    config = load_module(config_filepath)
    config.config_filepath = Path(config_filepath)
    config.script_filepath = Path(script_filepath)
    return config


def _check_script(module):
    if "run" not in module.__dict__:
        raise RuntimeError("Script file '{}' should contain a method `run(config, **kwargs)`".format(module.__file__))

    run_fn = module.__dict__['run']

    if not callable(run_fn):
        raise RuntimeError("Run method from script file '{}' should be a callable function".format(module.__file__))

    # Check the signature
    exception_msg = None
    kwargs = {}
    config = None
    logger = None
    if sys.version_info[0] < 3:
        try:
            callable_ = run_fn if hasattr(run_fn, '__name__') else run_fn.__call__
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
