# Python Configuration and a command line Runner

[![CircleCI](https://circleci.com/gh/vfdev-5/py_config_runner/tree/master.svg?style=svg)](https://circleci.com/gh/vfdev-5/py_config_runner/tree/master)
[![codecov](https://codecov.io/gh/vfdev-5/py_config_runner/branch/master/graph/badge.svg)](https://codecov.io/gh/vfdev-5/py_config_runner)
[![Documentation Status](https://readthedocs.org/projects/py-config-runner/badge/?version=latest)](https://py-config-runner.readthedocs.io/en/latest/?badge=latest)
[![image](https://img.shields.io/badge/dynamic/json.svg?label=PyPI&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fpy_config_runner%2Fjson&query=%24.info.version&colorB=brightgreen&prefix=v)](https://pypi.org/project/py-config-runner/)


Python configuration file and command line executable to run a script with.

**Why a python file as configuration?**

- Configuration of any complexity
- No need to serialize the configuration
- No need other meta-languages for the configuration


## Usage

### In the code

Configuration file (e.g. `config.py`):
```python
num_epochs = 100
batch_size = 256

model = resnet18(10)
train_loader = get_train_loader("/path/to/dataset", batch_size=batch_size)
unsup_dataloader = get_train_unsup_loader("/path/to/unsup_dataset", batch_size=batch_size)
...
```

Script file (e.g. `training.py`):
```python
from torch.utils.data import DataLoader
from py_config_runner import ConfigObject, TrainvalConfigSchema


class SSLTrainvalConfigSchema(TrainvalConfigSchema):

    unsup_dataloader: DataLoader



def training(config):
    # ...
    print(config.config_filepath)
    print(config.output_path)
    print(config.num_epochs)
    print(config.model)
    print(len(config.train_loader))


def main():

    config_filepath = "/path/to/config.py"
    config = ConfigObject(config_filepath)

    SSLTrainvalConfigSchema.validate(config)

    # Add more things at runtime    
    config.output_path = "/tmp/output"

    training(config)

```


### With launcher

```bash
cd /path/to/my/project
py_config_runner scripts/training.py configs/train/baseline.py
```

or

```bash
cd /path/to/my/project
python -u -m py_config_runner scripts/training.py configs/train/baseline.py
```

or if your specific launcher requires only python script files:
 
```bash
cd /path/to/my/project
python -m special_launcher `py_config_runner_script` scripts/training.py configs/train/baseline.py
```


The only condition on the script file is it should contain `run(config, **kwargs)` callable method. Additionally, 
argument kwargs contains `logger` (e.g. `kwargs['logger']`) and `local_rank` (e.g. `kwargs['logger']`) 
for distributed computations.


No restrictions are applied on the configuration file. It is user's responsibility to provide the script file that can 
consume given configuration file. Provided configuration file is loaded as python module and exposed into the script as 
the module named `config`.

### Examples

- [Example for Machine/Deep Learning](examples/README.md)

## Installation

```bash
pip install py-config-runner
```
