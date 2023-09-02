from typing import Union, Any
import pytest

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader

    has_torch = True
except ImportError:
    has_torch = False

from py_config_runner.config_utils import Schema, Iterable, BaseConfigSchema
from py_config_runner import ConfigObject, get_params


def setup_config(config_file):
    config = ConfigObject(config_file)
    config.seed = 12
    config.debug = True
    config.device = "cpu"
    config.num_epochs = 12

    if has_torch:
        config.model = torch.nn.Linear(1, 1)
        config.criterion = torch.nn.CrossEntropyLoss()
        config.optimizer = 123
        config.train_loader = [1, 2, 3]

    return config


def test_base_config_schema(config_filepath):
    config = setup_config(config_filepath)
    BaseConfigSchema.validate(config)


@pytest.mark.skipif(not has_torch, reason="No torch installed")
def test_schema_example(config_filepath):
    config = setup_config(config_filepath)

    class TrainingConfigSchema(Schema):
        seed: int
        debug: bool = False
        device: str = "cuda"

        train_loader: Union[DataLoader, Iterable]

        num_epochs: int
        model: torch.nn.Module
        optimizer: Any
        criterion: torch.nn.Module

    TrainingConfigSchema(**config)
    TrainingConfigSchema.validate(config)


def test_get_params_base(config_filepath):
    config = setup_config(config_filepath)
    params = get_params(config, BaseConfigSchema)

    assert isinstance(params, dict)
    assert params.get("seed", None) == config.seed
    assert params.get("debug", None) == config.debug

    with pytest.warns(UserWarning, match=r"This helper method is deprecated and will be removed"):
        params = get_params(config, (("seed", int), ("debug", bool)))
        assert isinstance(params, dict)
        assert params.get("seed", None) == config.seed
        assert params.get("debug", None) == config.debug


@pytest.mark.skipif(not has_torch, reason="No torch installed")
def test_get_params_training(config_filepath):
    config = setup_config(config_filepath)

    class TrainingConfigSchema(Schema):
        seed: int
        debug: bool = False
        device: str = "cuda"

        train_loader: Union[DataLoader, Iterable]

        num_epochs: int
        model: torch.nn.Module
        optimizer: Any
        criterion: torch.nn.Module

    params = get_params(config, TrainingConfigSchema)

    assert isinstance(params, dict)
    for k in ["seed", "debug", "device", "num_epochs"]:
        assert params.get(k, None) == config[k]

    assert params.get("train_loader", None) == len(config["train_loader"])
    assert params.get("model", None) in str(config["model"])
    assert params.get("criterion", None) in str(config["criterion"])
    assert params.get("optimizer", None) == config["optimizer"]
