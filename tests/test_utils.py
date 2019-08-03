import os
import tempfile
import logging
import shutil

from config_runner.utils import setup_logger, set_seed, load_module, add_logger_filehandler

import pytest


@pytest.fixture
def dirname():
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


def test_setup_logger(capsys):

    logger = logging.getLogger("test")
    log_level = logging.INFO
    setup_logger(logger, log_level)

    msg = "This is test message {}".format(123)
    logger.info(msg)

    captured = capsys.readouterr()
    err = captured.err.split('\r')
    err = list(map(lambda x: x.strip(), err))
    err = list(filter(None, err))
    assert "|test|INFO| " + msg in err[-1]


def test_set_seed():

    # check numpy tensor
    import numpy as np
    np.random.seed(0)
    a1 = np.random.rand(4, 10)
    a2 = np.random.rand(4, 10)

    set_seed(0)
    b1 = np.random.rand(4, 10)
    b2 = np.random.rand(4, 10)

    assert np.all(a1 == b1)
    assert np.all(a2 == b2)

    # check random
    import random
    random.seed(0)
    a1 = random.randint(0, 100)
    a2 = random.randint(0, 100)

    set_seed(0)
    b1 = random.randint(0, 100)
    b2 = random.randint(0, 100)

    assert a1 == b1
    assert a2 == b2

    # check torch tensors
    import torch

    torch.manual_seed(0)
    a1 = torch.randint(0, 100, size=(10, ))
    a2 = torch.randint(0, 100, size=(10, ))

    set_seed(0)
    b1 = torch.randint(0, 100, size=(10, ))
    b2 = torch.randint(0, 100, size=(10, ))

    assert torch.all(a1 == b1)
    assert torch.all(a2 == b2)


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


def test_add_logger_filehandler(dirname):
    logger = logging.getLogger("test")
    log_level = logging.DEBUG
    setup_logger(logger, log_level)

    filepath = os.path.join(dirname, "test.log")
    add_logger_filehandler(logger, filepath)

    msg1 = "This is a warning message {}".format(123)
    msg2 = "This is an info message {}".format(123)
    msg3 = "This is a debug message {}".format(123)
    logger.warning(msg1)
    logger.info(msg2)
    logger.debug(msg3)

    with open(filepath, 'r') as h:
        data = h.readlines()

    assert len(data) == 3
    assert "|test|WARNING| " + msg1 in data[0]
    assert "|test|INFO| " + msg2 in data[1]
    assert "|test|DEBUG| " + msg3 in data[2]
