# Examples for Machine/Deep Learning

## Requirements

```
pip install py_config_runner numpy
# Optional for the example with PyTorch
pip install torch torchvision
# Optional for the example with PyTorch-Ignite
pip install torch torchvision pytorch-ignite
```

## Basic example

```
cd basic
```

- [`main.py`](basic/main.py): entrypoint script with argparse accepts a configuration file and
uses `py_config_runner.ConfigObject` to parse python configuration file.

- [`training.py`](basic/training.py): module defines `run` method and how configuration is consumed.

- [configs/baseline_train.py](basic/configs/baseline_train.py): python configuration file.


### Python configuration in your script

```
python -u main.py --config=configs/baseline_train.py
```

### Python configuration and runner

```
py_config_runner training.py configs/baseline_train.py
```

## Deep learning example with PyTorch

```
cd pytorch
```

- [`main.py`](pytorch/main.py): entrypoint script with argparse accepts a configuration file and
uses `py_config_runner.ConfigObject` to parse python configuration file.

- [`training.py`](pytorch/training.py): module defines `run` method and how configuration is consumed.

- [configs/baseline_train_pytorch.py](pytorch/configs/baseline_train_pytorch.py): python configuration file with PyTorch model/optimizer/criterion etc.


### Python configuration in your script

```
python -u main.py --config=configs/baseline_train_pytorch.py
```

### Python configuration and runner

```
py_config_runner training.py configs/baseline_train_pytorch.py
```

## Deep learning example with PyTorch-Ignite

Distributed computations example using `py_config_runner.ConfigObject` (on CPU).

```
cd ignite
```

- [`main.py`](ignite/main.py): entrypoint script with argparse accepts a configuration file and
uses `py_config_runner.ConfigObject` to parse python configuration file.

- [configs/baseline_train_pytorch.py](ignite/configs/baseline_train_pytorch.py): python configuration file with PyTorch model/optimizer/criterion etc.


### Run with `torchrun`

```
torchrun --nproc_per_node=2 main.py --config=configs/baseline_train_pytorch.py
```

### Spawn processes from `main.py`

```
python -u main.py --config=configs/baseline_train_pytorch.py --nproc_per_node=2
```
