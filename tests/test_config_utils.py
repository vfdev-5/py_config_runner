from numbers import Integral, Number

from config_runner.config_utils import assert_config, get_params, BASE_CONFIG

import pytest


class _Config:
    pass


def test_assert_config():

    config = _Config()
    config.a = "a"
    config.b = "b"
    config.c = 1234

    with pytest.raises(TypeError,
                       match=r"Argument required_fields should be a Sequence of"):
        assert_config(config, 1234)

    with pytest.raises(ValueError,
                       match=r"Entries of required_fields should be"):
        assert_config(config, (1, 2, 3))

    required_fields = (
        ("a", str),
        ("b", str),
        ("c", Number),
        ("d", float)
    )

    with pytest.raises(ValueError,
                       match=r"Config should have attribute:"):
        assert_config(config, required_fields)

    config.d = "123"

    with pytest.raises(TypeError,
                       match=r"should be of type"):
        assert_config(config, required_fields)

    config.d = 12.34
    assert_config(config, required_fields)


def test_get_params():
    config = _Config()
    config.seed = 1234
    config.debug = True

    params = get_params(config, BASE_CONFIG)
    assert 'seed' in params
    assert 'debug' in params


def test_get_train_params():

    from config_runner.config_utils import TRAIN_CONFIG
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader

    config = _Config()
    config.seed = 1234
    config.debug = True
    config.device = "cpu"
    config.model = nn.Linear(1, 1)
    config.num_epochs = 1
    config.criterion = nn.CrossEntropyLoss()
    config.optimizer = optim.SGD(config.model.parameters(), lr=0.1)

    data = [1, 2, 3, 4, 5]
    config.train_loader = DataLoader(data, batch_size=1)

    params = get_params(config, TRAIN_CONFIG)
    assert 'train loader' in params
    assert 'train loader batch size' in params
