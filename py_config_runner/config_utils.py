from numbers import Number
from collections.abc import Iterable
from typing import Any, Union, Optional, Sequence, Type, Dict
from pydantic import BaseModel

try:
    import torch
    from torch.utils.data import DataLoader

    has_torch = True
except ImportError:
    has_torch = False

from py_config_runner.utils import ConfigObject
from py_config_runner.deprecated import assert_config, BASE_CONFIG, get_params as deprecated_get_params


class Schema(BaseModel):
    """Base class for all custom configuration schemas

    Example:

    .. code-block:: python

        from typing import *
        import torch
        from torch.utils.data import DataLoader
        from py_config_runner import Schema


        class TrainingConfigSchema(Schema):

            seed: int
            debug: bool = False
            device: str = "cuda"

            train_loader: Union[DataLoader, Iterable]

            num_epochs: int
            model: torch.nn.Module
            optimizer: Any
            criterion: torch.nn.Module

        config = ConfigObject("/path/to/config.py")
        # Check the config
        TrainingConfigSchema.validate(config)
    """

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def validate(cls, config: ConfigObject) -> "Schema":
        return cls(**config)


class BaseConfigSchema(Schema):
    """Base configuration schema.

    Schema defines required parameters:
        - seed (int)
        - debug (bool), default False

    """

    seed: int
    debug: bool = False


if has_torch:

    from py_config_runner.deprecated import TORCH_DL_BASE_CONFIG, TRAIN_CONFIG, TRAINVAL_CONFIG, INFERENCE_CONFIG

    class TorchModelConfigSchema(BaseConfigSchema):
        """Base configuration schema with a PyTorch model. Derived from
        :class:`py_config_runner.config_utils.BaseConfigSchema`.

        This schema is available only if torch is installed.

        Schema defines required parameters:
            - device (str), default "cuda"
            - model (torch.nn.Module)

        """

        device: str = "cuda"
        model: torch.nn.Module

    class TrainConfigSchema(TorchModelConfigSchema):
        """Training configuration schema with a PyTorch model. Derived from
        :class:`py_config_runner.config_utils.TorchModelConfigSchema`.

        This schema is available only if torch is installed.

        Schema defines required parameters:
            - train_loader (torch DataLoader or Iterable)
            - num_epochs (int)
            - criterion (torch.nn.Module)
            - optimizer (Any)
        """

        train_loader: Union[DataLoader, Iterable]
        num_epochs: int
        criterion: torch.nn.Module
        optimizer: Any

    class TrainvalConfigSchema(TrainConfigSchema):
        """Training/Validation configuration schema with a PyTorch model. Derived from
        :class:`py_config_runner.config_utils.TrainConfigSchema`.

        This schema is available only if torch is installed.

        Schema defines required parameters:
            - train_eval_loader (torch DataLoader or Iterable)
            - val_loader (torch DataLoader or Iterable)
            - lr_scheduler (Any)
        """

        train_eval_loader: Optional[Union[DataLoader, Iterable]]
        val_loader: Union[DataLoader, Iterable]
        lr_scheduler: Any

    class InferenceConfigSchema(TorchModelConfigSchema):
        """Inference configuration schema with a PyTorch model. Derived from
        :class:`py_config_runner.config_utils.TorchModelConfigSchema`.

        This schema is available only if torch is installed.

        Schema defines required parameters:
            - data_loader (torch DataLoader or Iterable)
            - weights_path (str)
        """

        data_loader: Union[DataLoader, Iterable]
        weights_path: str


def get_params(config: ConfigObject, required_fields: Union[Type[Schema], Sequence]) -> Dict:
    """Method to convert configuration into a dictionary matching `required_fields`.

    Args:
        config: configuration object
        required_fields (Type[Schema] or Sequence of (str, type)): Required attributes that should exist
            in the configuration. Either can accept a Schema class or a sequence of pairs
            ``(("a", (int, str)), ("b", str),)``.

    Returns:
        a dictionary

    Example:

    .. code-block:: python

        from typing import *
        import torch
        from torch.utils.data import DataLoader
        from py_config_runner import Schema


        class TrainingConfigSchema(Schema):

            seed: int
            debug: bool = False
            device: str = "cuda"

            train_loader: Union[DataLoader, Iterable]

            num_epochs: int
            model: torch.nn.Module
            optimizer: Any
            criterion: torch.nn.Module

        config = ConfigObject("/path/to/config.py")
        # Get config required parameters
        print(get_params(config, TrainingConfigSchema))
        # >
        # {"seed": 12, "debug": False, "device": "cuda", ...}

    """

    if isinstance(required_fields, Sequence):
        return deprecated_get_params(config, required_fields)

    if not (isinstance(required_fields, type) and issubclass(required_fields, Schema)):
        raise ValueError("Argument required_fields should be a class (not instance) derived from Schema")

    result = required_fields.validate(config)
    params = {}
    for k, v in result.dict().items():
        if isinstance(v, (Number, str, bool)):
            params[k] = v
        elif hasattr(v, "__len__"):
            params[k] = len(v)  # type: ignore[assignment]
            if hasattr(v, "batch_size"):
                params["{} batch size".format(k)] = v.batch_size
        elif hasattr(v, "__class__"):
            params[k] = v.__class__.__name__

    return params
