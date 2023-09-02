import argparse
from pathlib import Path

from py_config_runner import ConfigObject

from training import run


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Example application")
    parser.add_argument("--config", type=Path, help="Input configuration file")
    args = parser.parse_args()

    assert args.config is not None
    assert args.config.exists()

    # Pass configuration file into py_config_runner.ConfigObject
    # and fetch configuration parameters as attributes
    # see inside run() function
    config = ConfigObject(args.config)

    run(config)
