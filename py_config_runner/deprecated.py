import logging
import warnings

LOGGING_FORMATTER = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s| %(message)s")


def setup_logger(logger, level=logging.INFO):
    """DEPRECATED. Resets formatting and stdout stream handler to the logger

    Args:
        logger: logger from `logging` module
        level: logging verbosity level

    """
    warnings.warn("This helper method is deprecated and will be removed in 0.3.0")

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
    """DEPRECATED. Adds additional file handler to the logger

    Args:
        logger: logger from `logging` module
        filepath: output logging file

    """
    warnings.warn("This helper method is deprecated and will be removed in 0.3.0")

    # create file handler which logs even debug messages
    fh = logging.FileHandler(filepath)
    fh.setLevel(logger.level)
    fh.setFormatter(LOGGING_FORMATTER)
    logger.addHandler(fh)


def set_seed(seed):
    """DEPRECATED. Setup seed for numpy, random, torch

    Args:
        seed (int): any integer random seed

    """
    warnings.warn("This helper method is deprecated and will be removed in 0.3.0")

    import random
    import numpy as np
    import torch

    random.seed(seed)
    torch.manual_seed(seed)
    np.random.seed(seed)
