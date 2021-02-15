import os
import pytest
from pathlib import Path

from py_config_runner import ConfigObject, load_module


def test_config_object(config_filepath):

    config = ConfigObject(config_filepath)
    assert "a" in config
    assert config["a"] == config.a == config.get("a") == 1
    assert "b" in config
    assert config["b"] == config.b == config.get("b") == 2

    config.c = 3
    config["d"] = 4

    assert "c" in config
    assert config["c"] == config.c == config.get("c") == 3
    assert config["d"] == config.d == config.get("d") == 4
    assert "config_filepath" in config
    assert isinstance(config.config_filepath, Path)
    assert config.config_filepath == config_filepath
    assert config["config_filepath"] == config_filepath
    assert config.get("config_filepath") == config_filepath

    for k in config:
        assert not k.startswith("__")

    def foo(**kwargs):
        for k in ["a", "b", "c", "d", "config_filepath"]:
            assert k in kwargs

    foo(**config)


def test_config_object_length(config_filepath):
    config = ConfigObject(config_filepath)

    assert len(config) == 4 + 1  # config + config_filepath


def test_config_object_items(config_filepath):
    config = ConfigObject(config_filepath)

    res = [(k, v) for k, v in config.items()]
    assert len(res) == 4 + 1  # config + config_filepath


def test_config_object_loading(config_filepath):
    config = ConfigObject(config_filepath)

    def foo(**kwargs):
        for k in ["a", "b", "config_filepath"]:
            assert k in kwargs

    foo(**config)


def test_config_object_repr(config_filepath):
    config = ConfigObject(config_filepath)

    out = repr(config)
    assert "a" in out
    assert "b" in out
    assert "data" in out
    assert "_data" in out


def test_load_module(dirname):
    import numpy as np

    filepath = os.path.join(dirname, "custom_module.py")

    s = """
import numpy as np
a = 123
b = np.array([1, 2, 3])
    """

    with open(filepath, "w") as h:
        h.write(s)

    custom_module = load_module(filepath)

    assert "a" in custom_module.__dict__
    assert custom_module.a == 123

    assert "b" in custom_module.__dict__
    assert np.all(custom_module.b == np.array([1, 2, 3]))


def test_load_module_wrong_args():
    with pytest.raises(ValueError, match=r"is not found"):
        load_module("/tmp/abcdef")

    with pytest.raises(ValueError, match=r"should be a file"):
        load_module("/tmp/")
