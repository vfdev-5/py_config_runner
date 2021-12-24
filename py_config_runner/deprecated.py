import logging
import warnings
from collections.abc import Iterable, Sequence
from numbers import Integral, Number

try:
    import torch
    from torch.utils.data import DataLoader

    has_torch = True
except ImportError:
    has_torch = False


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


def assert_config(config, required_fields):
    """DEPRECATED. Method to check the config if it has required fields of specified type

    Args:
        config: Configuration object to check
        required_fields (Sequence of (str, type)): Required attributes that should exist in the configuration.
    """
    warnings.warn("This helper method is deprecated and will be removed in 0.3.0")

    if not isinstance(required_fields, Sequence):
        raise TypeError(
            "Argument required_fields should be a Sequence of (str, type), "
            "but given {}".format(type(required_fields))
        )
    for field in required_fields:
        if not (isinstance(field, Sequence) and len(field) == 2):
            raise ValueError("Entries of required_fields should be (str, type), but given {}".format(type(field)))
        k, t = field
        obj = getattr(config, k, None)
        if obj is None:
            raise ValueError("Config should have attribute: {} of type {}".format(k, t))
        if t is not None:
            if not isinstance(obj, t):
                raise TypeError("config.{} should be of type {}, but given {}".format(k, t, type(obj)))


def get_params(config, required_fields):
    """Method to convert configuration into a dictionary matching `required_fields`.

    Args:
        config: configuration object
        required_fields (Sequence of (str, type)): Required attributes that should exist in the configuration.
            For example, `(("a", (int, str)), ("b", str),)`

    Returns:
        a dictionary

    """
    assert_config(config, required_fields)
    params = {}
    for k, _ in required_fields:
        obj = getattr(config, k)
        k = k.replace("_", " ")
        if isinstance(obj, (Number, str, bool)):
            params[k] = obj
        elif hasattr(obj, "__len__"):
            params[k] = len(obj)
            if hasattr(obj, "batch_size"):
                params["{} batch size".format(k)] = obj.batch_size
        elif hasattr(obj, "__class__"):
            params[k] = obj.__class__.__name__

    return params


BASE_CONFIG = (
    ("seed", Integral),
    ("debug", bool),
)


if has_torch:

    TORCH_DL_BASE_CONFIG = BASE_CONFIG + (
        ("device", str),
        ("model", torch.nn.Module),
    )

    TRAIN_CONFIG = TORCH_DL_BASE_CONFIG + (
        ("train_loader", (DataLoader, Iterable)),
        ("num_epochs", Integral),
        ("criterion", torch.nn.Module),
        ("optimizer", torch.optim.Optimizer),
    )

    TRAINVAL_CONFIG = TRAIN_CONFIG + (
        ("train_eval_loader", (DataLoader, Iterable)),
        ("val_loader", (DataLoader, Iterable)),
        ("lr_scheduler", object),
    )

    INFERENCE_CONFIG = TORCH_DL_BASE_CONFIG + (
        ("data_loader", (DataLoader, Iterable)),
        ("weights", str),
        ("training_run_uuid", str),
    )
