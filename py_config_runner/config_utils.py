
from collections.abc import Sequence, Iterable, Sized
from numbers import Integral, Number


def assert_config(config, required_fields):
    """Method to check the config if it has required fields of specified type

    Args:
        config: Configuration object to check
        required_fields (Sequence of (str, type)): Required attributes that should exist in the configuration.
            For example, `(("a": (int, str)), ("b", str),)`
    """
    if not isinstance(required_fields, Sequence):
        raise TypeError("Argument required_fields should be a Sequence of (str, type), "
                        "but given {}".format(type(required_fields)))
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
            For example, `(("a": (int, str)), ("b", str),)`

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
                params['{} batch size'.format(k)] = obj.batch_size
        elif hasattr(obj, "__class__"):
            params[k] = obj.__class__.__name__

    return params


BASE_CONFIG = (
    ("seed", Integral),
    ("debug", bool),
)


class SizedIterable(Sized, Iterable):
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, C):
        if cls is SizedIterable:
            if any(m in B.__dict__ for B in C.__mro__
                   for m in ("__len__", "__iter__")):
                return True
        return NotImplemented


try:

    import torch
    from torch.utils.data import DataLoader

    TORCH_DL_BASE_CONFIG = BASE_CONFIG + (
        ("device", str),
        ("model", torch.nn.Module),
    )

    TRAIN_CONFIG = TORCH_DL_BASE_CONFIG + (
        ("train_loader", (DataLoader, SizedIterable)),
        ("num_epochs", Integral),
        ("criterion", torch.nn.Module),
        ("optimizer", torch.optim.Optimizer),
    )

    TRAINVAL_CONFIG = TRAIN_CONFIG + (
        ("train_eval_loader", (DataLoader, SizedIterable)),
        ("val_loader", (DataLoader, SizedIterable)),
        ("lr_scheduler", object)
    )

    INFERENCE_CONFIG = TORCH_DL_BASE_CONFIG + (
        ("data_loader", (DataLoader, SizedIterable)),
        ("weights", str),
        ("training_run_uuid", str),
    )


except ImportError:
    import warnings
    warnings.warn("As no torch module found, TRAIN_CONFIG, INFERENCE_CONFIG are not defined. Please install pytorch")
