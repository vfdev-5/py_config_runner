from torch import nn
from torch.optim import SGD
from torchvision.transforms import Compose, ToTensor, Normalize, RandomHorizontalFlip
from torchvision.models import resnet18

# module from the example
from utils import get_mnist_data_loaders

seed = 12
debug = False
train_batch_size = 64
val_batch_size = 128

parameter_c = 123.45


train_transform = Compose([RandomHorizontalFlip(), ToTensor(), Normalize((0.1307,), (0.3081,))])
val_transform = Compose([ToTensor(), Normalize((0.1307,), (0.3081,))])

train_loader, val_loader = get_mnist_data_loaders(train_transform, train_batch_size, val_transform, val_batch_size)

model = resnet18(num_classes=10)

optimizer = SGD(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

num_epochs = 20
val_interval = 5
