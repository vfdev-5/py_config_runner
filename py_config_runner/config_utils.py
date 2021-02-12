from collections.abc import Iterable
from typing import Any, Union, Optional
from pydantic import BaseModel

try:
    import torch
    from torch.utils.data import DataLoader

    has_torch = True
except ImportError:
    has_torch = False

from py_config_runner.utils import ConfigObject
from py_config_runner.deprecated import assert_config, get_params, BASE_CONFIG


class Schema(BaseModel):
    """Base class for all custom configuration schemas

    Example:

    .. code-block:: python

        from typing import *
        import torch
        from torch.utils.data import DataLoader
        from py_config_runner import Schema
        from py_config_runner.config_utils import SizedIterable


        class TrainingConfigSchema(Schema):

            seed: int
            debug: bool = False
            device: str = "cuda"

            train_loader: Union[DataLoader, SizedIterable]

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
    def validate(cls, config):
        return cls(**config)


class BaseConfigSchema(Schema):
    seed: int
    debug: bool = False


if has_torch:

    from py_config_runner.deprecated import TORCH_DL_BASE_CONFIG, TRAIN_CONFIG, TRAINVAL_CONFIG, INFERENCE_CONFIG

    class TorchModelConfigSchema(BaseConfigSchema):
        device: str
        model: torch.nn.Module

    class TrainConfigSchema(TorchModelConfigSchema):
        train_loader: Union[DataLoader, Iterable]
        num_epochs: int
        criterion: torch.nn.Module
        optimizer: Any

    class TrainvalConfigSchema(TrainConfigSchema):
        train_eval_loader: Optional[Union[DataLoader, Iterable]]
        val_loader: Union[DataLoader, Iterable]
        lr_scheduler: Any

    class InferenceConfigSchema(TorchModelConfigSchema):
        data_loader: Union[DataLoader, Iterable]
        weights: str
        training_run_id: str
