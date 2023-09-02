import inspect
import os
import pytest
import multiprocessing as mp
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

    for k, v in config.__dict__.items():
        assert not inspect.ismodule(v)


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
    filepath = dirname / "bad_config.py"

    s = """
a = 123

raise RuntimeError("error")
    """

    with filepath.open("w") as h:
        h.write(s)

    config = ConfigObject(filepath)

    with pytest.raises(RuntimeError, match=r"error"):
        assert config.a == 123


def test_config_object_mutations(dirname):
    filepath = dirname / "custom_module.py"

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

    with filepath.open("w") as h:
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


@pytest.mark.parametrize(
    "old_value",
    [{"encoder": "E1", "decoder": "D1"}, "unet", [1, 2, 3], 5],
)
@pytest.mark.parametrize(
    "new_value",
    ["unet", [1, 2, 3], {"encoder": "E1", "decoder": "D1"}, 5],
)
def test_config_object_mutations_nonconst(old_value, new_value, dirname):
    filepath = dirname / "custom_module.py"

    s = f"""

a = {old_value}

    """

    with filepath.open("w") as h:
        h.write(s)

    config = ConfigObject(filepath, mutations={"a": new_value})

    assert config.a == new_value


def test_config_object_mutations_assert(config_filepath):
    with pytest.raises(TypeError, match=r"Argument mutations should be a mapping"):
        ConfigObject(config_filepath, mutations="abc")

    class A:
        pass

    with pytest.raises(ValueError, match=r"Failed to create value's AST"):
        ConfigObject(config_filepath, mutations={"a": A()})


@pytest.mark.parametrize("mutations", [None, {"a": [1, 2, 3]}])
def test_config_object_no_modules(mutations, config_filepath2):
    import numpy as np

    config = ConfigObject(config_filepath2, mutations=mutations)

    for k, v in config.items():
        assert not inspect.ismodule(v), f"{k}: {v}"

    assert "a" in config
    assert config.a == 1 if mutations is None else [1, 2, 3]
    assert "arr" in config
    np.testing.assert_allclose(config.arr, np.array([1, 2, 3]))
    assert "out" in config
    assert config.out == 12


def test_config_object_mutations_validate(dirname):
    filepath = dirname / "custom_module.py"

    s = """

a = 123

def func(x):
    return x + a

out = func(10)
    """

    with filepath.open("w") as h:
        h.write(s)

    config = ConfigObject(filepath, mutations={"a": 333, "b": 22.0})

    with pytest.raises(RuntimeError, match=r"Following mutations were not applied"):
        assert config.a == 333


def test_load_module(dirname):
    import numpy as np

    filepath = dirname / "custom_module.py"

    s = """
import numpy as np
a = 123
b = np.array([1, 2, 3])
    """

    with filepath.open("w") as h:
        h.write(s)

    custom_module = load_module(filepath)

    assert "a" in custom_module.__dict__
    assert custom_module.a == 123

    assert "b" in custom_module.__dict__
    np.testing.assert_allclose(custom_module.b, np.array([1, 2, 3]))


def test_load_module_wrong_args():
    with pytest.raises(ValueError, match=r"is not found"):
        load_module("/tmp/abcdef")

    with pytest.raises(ValueError, match=r"should be a file"):
        load_module("/tmp/")


def worker_function(config):
    pass


@pytest.mark.parametrize("method", ["fork", "spawn"])
def test_mp_config(method, config_filepath):
    config = ConfigObject(config_filepath)
    ctx = mp.get_context(method)
    p = ctx.Process(target=worker_function, args=(config,))
    p.start()
    p.join()


def worker_config_checker(config):
    import numpy as np

    assert "a" in config
    assert config.a == 123

    assert "b" in config
    np.testing.assert_allclose(config.b, np.array([1, 2, 3]))

    assert "out" in config
    assert config.out == 12


@pytest.mark.parametrize("method", ["fork", "spawn"])
def test_mp_config2(method, config_filepath2):
    config = ConfigObject(config_filepath2)
    ctx = mp.get_context(method)
    p = ctx.Process(target=worker_config_checker, args=(config,))
    p.start()
    p.join()
