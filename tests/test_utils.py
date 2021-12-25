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
    assert config["_data"] == config._data == config.get("_data") == 3

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


def test_config_object_init_kwargs(config_filepath):
    # Pass a as kwargs
    config = ConfigObject(config_filepath, a=10, another_data=123)
    # assert that a is overriden by config_filepath
    assert config.a == 1
    assert config.another_data == 123


def test_config_object_lazy_load(dirname):
    filepath = os.path.join(dirname, "bad_config.py")

    s = """
a = 123

raise RuntimeError("error")
    """

    with open(filepath, "w") as h:
        h.write(s)

    config = ConfigObject(filepath)

    with pytest.raises(RuntimeError, match=r"error"):
        assert config.a == 123


def test_config_object_mutations(dirname):
    filepath = os.path.join(dirname, "custom_module.py")

    s = """

a = 123
b = 12.3
c = "abc"
d = True
# e = None


def func(x):
    return x + a

out = func(10)

def func2(x):
    return x + b

out2 = func2(1.0)


def func3(x):
    if x == "abc":
        return 1.0
    elif x == "cba":
        return -1.0
    else:
        return 0.0

out3 = func3(c)


out4 = 10 if d else -10
# out5 = 10 if e is None else -10
    """

    with open(filepath, "w") as h:
        h.write(s)

    config = ConfigObject(filepath, mutations={"a": 333, "b": 22.0, "c": "cba", "d": False})

    assert config.a == 333
    assert config.out == 10 + 333
    assert config.b == 22.0
    assert config.out2 == 1.0 + 22.0
    assert config.c == "cba"
    assert config.out3 == -1.0
    assert not config.d
    assert config.out4 == -10


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
