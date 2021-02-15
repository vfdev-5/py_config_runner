# Examples for Machine/Deep Learning

## Requirements

```
pip install py_config_runner numpy
# Optional
pip install torch torchvision
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

- [`main.py`](basic/main.py): entrypoint script with argparse accepts a configuration file and 
uses `py_config_runner.ConfigObject` to parse python configuration file.

- [`training.py`](basic/training.py): module defines `run` method and how configuration is consumed.

- [configs/baseline_train_pytorch.py](basic/configs/baseline_train_pytorch.py): python configuration file.


### Python configuration in your script

```
python -u main.py --config=configs/baseline_train_pytorch.py
```

### Python configuration and runner

```
py_config_runner training.py configs/baseline_train_pytorch.py
```
