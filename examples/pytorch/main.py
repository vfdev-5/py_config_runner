import argparse
from pathlib import Path

from py_config_runner import ConfigObject

from training import run


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Example application")
    parser.add_argument("--config", type=Path, help="Input configuration file")
    parser.add_argument("--bs", type=int, default=None, help="Override train batch size")
    parser.add_argument("--lr", type=float, default=None, help="Override train learning rate")
    parser.add_argument("--ep", type=int, default=None, help="Override number of epochs")
    args = parser.parse_args()

    assert args.config is not None
    assert args.config.exists()

    # Define configuration mutations if certain cmd args are defined
    mutations = {}
    if args.bs is not None:
        mutations["train_batch_size"] = args.bs
    if args.lr is not None:
        mutations["learning_rate"] = args.lr
    if args.ep is not None:
        mutations["num_epochs"] = args.ep

    if len(mutations) < 1:
        mutations = None

    # Pass configuration file into py_config_runner.ConfigObject
    # and fetch configuration parameters as attributes
    # see inside run() function
    config = ConfigObject(args.config, mutations=mutations)

    run(config)
