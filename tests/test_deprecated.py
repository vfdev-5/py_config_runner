from numbers import Number
import pytest

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader

    has_torch = True
except ImportError:
    has_torch = False


from py_config_runner.deprecated import assert_config, get_params, BASE_CONFIG


class _Config:
    pass


def test_assert_config():

    config = _Config()
    config.a = "a"
    config.b = "b"
    config.c = 1234

    with pytest.warns(UserWarning, match=r"This helper method is deprecated"):
        with pytest.raises(TypeError, match=r"Argument required_fields should be a Sequence of"):
            assert_config(config, 1234)

    with pytest.warns(UserWarning, match=r"This helper method is deprecated"):
        with pytest.raises(ValueError, match=r"Entries of required_fields should be"):
            assert_config(config, (1, 2, 3))

    required_fields = (("a", str), ("b", str), ("c", Number), ("d", float))

    with pytest.warns(UserWarning, match=r"This helper method is deprecated"):
        with pytest.raises(ValueError, match=r"Config should have attribute:"):
            assert_config(config, required_fields)

    config.d = "123"

    with pytest.warns(UserWarning, match=r"This helper method is deprecated"):
        with pytest.raises(TypeError, match=r"should be of type"):
            assert_config(config, required_fields)

    with pytest.warns(UserWarning, match=r"This helper method is deprecated"):
        config.d = 12.34
        assert_config(config, required_fields)


def test_get_params():
    config = _Config()
    config.seed = 1234
    config.debug = True

    with pytest.warns(UserWarning, match=r"This helper method is deprecated"):
        params = get_params(config, BASE_CONFIG)
    assert "seed" in params
    assert "debug" in params


@pytest.mark.skipif(not has_torch, reason="No torch installed")
def test_get_train_params():

    from py_config_runner.config_utils import TRAIN_CONFIG

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

    with pytest.warns(UserWarning, match=r"This helper method is deprecated"):
        params = get_params(config, TRAIN_CONFIG)
    assert "train loader" in params
    assert "train loader batch size" in params
