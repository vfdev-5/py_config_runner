from typing import Any
from py_config_runner import Schema, get_params


try:
    import torch

    has_torch = True
except ImportError:
    has_torch = False


class MyTrainingConfigSchema(Schema):
    # Define my training config required parameters:
    # Type hints are from typing
    seed: int
    debug: bool
    parameter_c: float
    model: Any


def run(config, **kwargs):

    print()
