try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

import tempfile
import shutil

import pytest


@pytest.fixture
def dirname():
    path = tempfile.mkdtemp()
    yield Path(path)
    shutil.rmtree(path)


@pytest.fixture
def config_filepath():
    path = Path(tempfile.mkdtemp())
    config_filepath = path / "config.py"
    data = """
a = 1
b = 2
        """

    with config_filepath.open("w") as h:
        h.write(data)

    yield config_filepath
    shutil.rmtree(path.as_posix())


@pytest.fixture
def script_filepath():
    path = Path(tempfile.mkdtemp())
    script_filepath = path / "script.py"
    data = """

def run(config, **kwargs):
    print("Run")
    assert config.a == 1
    assert config.b == 2
    print(config.a)
    print(config.b)
    print(config.config_filepath.as_posix())
    print(config.script_filepath.as_posix())
        """

    with script_filepath.open("w") as h:
        h.write(data)

    yield script_filepath
    shutil.rmtree(path.as_posix())


@pytest.fixture
def logging_script_filepath():
    path = Path(tempfile.mkdtemp())
    script_filepath = path / "script.py"
    data = """

def run(config, logger=None, **kwargs):
    assert logger is not None

    logger.info("Start run script")
    logger.info(config.a)
    logger.info(config.b)
        """

    with script_filepath.open("w") as h:
        h.write(data)

    yield script_filepath
    shutil.rmtree(path.as_posix())


@pytest.fixture
def example_path():
    cwd = Path(__file__).parent
    p = cwd / "example"
    yield p


@pytest.fixture
def example_baseline_config(example_path):
    p = example_path / "configs" / "baseline.py"
    assert p.exists()
    yield p


@pytest.fixture
def example_scripts_training(example_path):
    p = example_path / "scripts" / "training.py"
    assert p.exists()
    yield p
