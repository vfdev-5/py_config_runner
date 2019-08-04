import os
from py_config_runner.runner import run_script

import pytest


def test_run_script_script_file_no_run(dirname):  # noqa: F811
    script_fp = os.path.join(dirname, "script.py")

    s = """
import numpy as np

a = 123
b = np.array([1, 2, 3])

    """

    with open(script_fp, "w") as h:
        h.write(s)

    with pytest.raises(RuntimeError, match="should contain a method `run"):
        run_script(script_fp, "")


def test_run_script_script_file_run_not_callable(dirname):  # noqa: F811
    script_fp = os.path.join(dirname, "script.py")

    s = """
run = 0
    """

    with open(script_fp, "w") as h:
        h.write(s)

    with pytest.raises(RuntimeError, match="should be a callable function"):
        run_script(script_fp, "")


def test_run_script_script_file_run_wrong_signature(dirname):  # noqa: F811
    script_fp = os.path.join(dirname, "script.py")

    s = """
def run():
    pass
    """

    with open(script_fp, "w") as h:
        h.write(s)

    with pytest.raises(RuntimeError, match="Run method signature should be"):
        run_script(script_fp, "")


def test_run_script(capsys, script_filepath, config_filepath):  # noqa: F811

    run_script(script_filepath, config_filepath)

    captured = capsys.readouterr()
    out = captured.out.split('\r')
    out = list(map(lambda x: x.strip(), out))
    out = list(filter(None, out))
    assert "Run\n1\n2\n{}\n{}".format(config_filepath, script_filepath) in out[-1]


def test_run_logging_script(capsys, logging_script_filepath, config_filepath):  # noqa: F811

    run_script(logging_script_filepath, config_filepath)

    captured = capsys.readouterr()
    out = captured.err.split('\n')
    out = list(map(lambda x: x.strip(), out))
    out = list(filter(None, out))
    assert "|script|INFO| Start run script" in out[0]
    assert "|script|INFO| 1" in out[1]
    assert "|script|INFO| 2" in out[2]


def test_run_script_raise_exeption(dirname, config_filepath):  # noqa: F811
    script_fp = os.path.join(dirname, "bad_script.py")

    s = """
def run(config, **kwargs):
    raise RuntimeError("STOP")
    """

    with open(script_fp, "w") as h:
        h.write(s)

    run_script(script_fp, config_filepath)
