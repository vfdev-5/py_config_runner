import logging


LOGGING_FORMATTER = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s| %(message)s")


def setup_logger(logger, level=logging.INFO):

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
    # create file handler which logs even debug messages
    fh = logging.FileHandler(filepath)
    fh.setLevel(logger.level)
    fh.setFormatter(LOGGING_FORMATTER)
    logger.addHandler(fh)


def set_seed(seed):
    import random
    import numpy as np
    import torch

    random.seed(seed)
    torch.manual_seed(seed)
    np.random.seed(seed)


def load_module(filepath):
    import importlib.util

    try:
        from pathlib import Path
    except ImportError:
        from pathlib2 import Path

    spec = importlib.util.spec_from_file_location(Path(filepath).stem, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
