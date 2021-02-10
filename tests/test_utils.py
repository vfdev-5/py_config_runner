import os
import pytest
from pathlib import Path

from py_config_runner import ConfigObject, load_module


def test_config_object(config_filepath):

    config = ConfigObject(config_filepath)
    assert "a" in config
    assert config["a"] == config.a == config.get("a")
    assert "b" in config
    assert config["b"] == config.b == config.get("b")

    config.c = 3
    config["d"] = 4

    assert "c" in config
    assert config["c"] == config.c == config.get("c")
    assert "config_filepath" in config
    assert isinstance(config.config_filepath, Path)
    assert config.config_filepath == config_filepath
    assert config["config_filepath"] == config_filepath
    assert config.get("config_filepath") == config_filepath


def test_load_module_inexisting_file():

    filepath = "/tmp/tmp.py"

    with pytest.raises(ValueError, match="is not found"):
        load_module(filepath)


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
