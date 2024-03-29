import os
from torch import nn
from torch.optim import SGD
from torchvision.transforms import Compose, ToTensor, Normalize, RandomHorizontalFlip
from torchvision.models import resnet18

# module from the example
from utils import get_mnist_datasets

seed = 12
debug = False
train_batch_size = 16
val_batch_size = 16


train_transform = Compose([RandomHorizontalFlip(), ToTensor(), Normalize((0.1307,), (0.3081,))])
val_transform = Compose([ToTensor(), Normalize((0.1307,), (0.3081,))])


path = os.getenv("DATASET_PATH", "/tmp/mnist")
train_set, val_set = get_mnist_datasets(path, train_transform, val_transform)

model = resnet18(num_classes=10)
model.conv1 = nn.Conv2d(1, 64, 3)

learning_rate = 0.01

optimizer = SGD(model.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss()

num_epochs = 3
val_interval = 2
