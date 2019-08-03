import os
import tempfile
import shutil

import pytest


@pytest.fixture
def dirname():
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture
def script_filepath():
    path = tempfile.mkdtemp()
    script_filepath = os.path.join(path, "script.py")
    data = """

def run(config, **kwargs):
    print("Run")
    print(config.a)
    print(config.b)
    print(config.config_filepath.as_posix())
    print(config.script_filepath.as_posix())
        """

    with open(script_filepath, "w") as h:
        h.write(data)

    yield script_filepath
    shutil.rmtree(path)


@pytest.fixture
def config_filepath():
    path = tempfile.mkdtemp()
    config_filepath = os.path.join(path, "config.py")
    data = """
a = 1
b = 2
        """

    with open(config_filepath, "w") as h:
        h.write(data)

    yield config_filepath
    shutil.rmtree(path)


@pytest.fixture
def logging_script_filepath():
    path = tempfile.mkdtemp()
    script_filepath = os.path.join(path, "script.py")
    data = """

def run(config, logger=None, **kwargs):
    assert logger is not None

    logger.info("Start run script")
    logger.info(config.a)
    logger.info(config.b)
        """

    with open(script_filepath, "w") as h:
        h.write(data)

    yield script_filepath
    shutil.rmtree(path)
