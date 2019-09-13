
from py_config_runner.utils import set_seed

from utils import foo


def run(config, **kwargs):

    print("Run example training")

    if hasattr(config, "setup"):
        config = config.setup()

    set_seed(config.seed)
    assert foo()
