# Examples for Machine/Deep Learning

## Requirements

```
pip install py_config_runner numpy
# Optional
pip install torch torchvision
```

## Python configuration in your script

```
python -u main.py --config=configs/baseline_train.py
```

If installed PyTorch
```
python -u main.py --config=configs/baseline_train_pytorch.py
```


## Python configuration and runner

```
py_config_runner training.py configs/baseline_train.py
```

If installed PyTorch
```
py_config_runner training.py configs/baseline_train_pytorch.py
```



For example, below configuration file defines a model, datasets, criterion, optimizer etc and the training script runs the training:

```python
# config.py
from torch import nn
from torch.optim import SGD

from torchvision.transforms import Compose, ToTensor, Normalize, RandomHorizontalFlip

from mymodule.dataflow import get_mnist_data_loaders
from another_module.models import CoolNet


train_transform=Compose([RandomHorizontalFlip(), ToTensor(), Normalize((0.1307,), (0.3081,))])
val_transform=Compose([ToTensor(), Normalize((0.1307,), (0.3081,))])

train_batch_size = 64
val_batch_size = 128

train_loader, val_loader = get_mnist_data_loaders(train_transform, train_batch_size, val_transform, val_batch_size)

model = CoolNet()

optimizer = SGD(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

num_epochs = 20

val_interval = 5
``` 

```python
# training.py
from mymodule.utils import prepare_batch
from mymodule.metrics import compute_running_accuracy


def run(config, **kwargs):
    
    model = config.model
    model.to('cuda')

    criterion = config.criterion
    criterion = criterion.to('cuda')
    
    optimizer = config.optimizer
    
    for e in range(config.num_epochs):
        print("Epoch {} / {}".format(e + 1, config.num_epochs))
        for batch in config.train_loader:
            x, y = prepare_batch(batch, 'cuda')                
            optimizer.zero_grad()
            y_pred = model(x)            
            loss = criterion(y_pred, y)
            loss.backward()
            optimizer.step()
            
        if e % config.val_metrics == 0:
            running_acc = 0
            for batch in config.val_loader:
                x, y = prepare_batch(batch, 'cuda')                                
                y_pred = model(x)            
                
                running_acc = compute_running_accuracy(running_acc, y_pred, y)
                
            print("Validation: metrics={}".format(running_acc))
```