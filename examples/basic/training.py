from typing import Any

import numpy as np

from py_config_runner import Schema, get_params


class MyTrainingConfigSchema(Schema):
    # Define required parameters for a training config
    # Type hints are from typing
    seed: int
    debug: bool
    n_in_features: int
    n_classes: int
    model: Any


def run(config, **kwargs):
    # Let's validate the config
    MyTrainingConfigSchema.validate(config)

    print("Configuration: ")
    for k, v in get_params(config, MyTrainingConfigSchema).items():
        print(f"\t{k}: {v}")

    # fetch parameters:
    model = config.model
    seed = config.seed
    debug = config.debug

    if debug:
        print("Seed: ", seed)
        print("Model: ", model)

    x = np.random.rand(4, config.n_in_features)
    y_preds = model(x)
    print("y_preds.shape:", y_preds.shape)
