import logging


LOGGING_FORMATTER = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s| %(message)s")


def setup_logger(logger, level=logging.INFO):
    """Resets formatting and stdout stream handler to the logger

    Args:
        logger: logger from `logging` module
        level: logging verbosity level

    """

    if logger.hasHandlers():
        for h in list(logger.handlers):
            logger.removeHandler(h)

    logger.setLevel(level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(LOGGING_FORMATTER)
    logger.addHandler(ch)


def add_logger_filehandler(logger, filepath):
    """Adds additional file handler to the logger

    Args:
        logger: logger from `logging` module
        filepath: output logging file

    """
    # create file handler which logs even debug messages
    fh = logging.FileHandler(filepath)
    fh.setLevel(logger.level)
    fh.setFormatter(LOGGING_FORMATTER)
    logger.addHandler(fh)


def set_seed(seed):
    """Setup seed for numpy, random, torch

    Args:
        seed (int): any integer random seed

    """
    import random
    import numpy as np
    import torch

    random.seed(seed)
    torch.manual_seed(seed)
    np.random.seed(seed)


def load_module(filepath):
    """Method to load module from file path

    Args:
        filepath: path to module to load

    """
    import importlib.util

    try:
        from pathlib import Path
    except ImportError:
        from pathlib2 import Path

    if not Path(filepath).exists():
        raise ValueError("File '{}' is not found".format(filepath))

    spec = importlib.util.spec_from_file_location(Path(filepath).stem, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
