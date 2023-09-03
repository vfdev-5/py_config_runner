from torch.utils.data import Subset
from torchvision.datasets import MNIST


def get_mnist_datasets(path, train_transform, val_transform):
    train_set = MNIST(download=True, root=path, transform=train_transform, train=True)
    # Reduce the dataset size for demo purposes
    train_set = Subset(train_set, indices=list(range(100)))
    val_set = MNIST(download=False, root=path, transform=val_transform, train=False)
    # Reduce the dataset size for demo purposes
    val_set = Subset(val_set, indices=list(range(100)))
    return train_set, val_set
