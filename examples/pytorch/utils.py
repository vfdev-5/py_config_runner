from torch.utils.data import DataLoader, Subset
from torchvision.datasets import MNIST


def get_mnist_data_loaders(path, train_transform, train_batch_size, val_transform, val_batch_size):
    train_set = MNIST(download=True, root=path, transform=train_transform, train=True)
    # Reduce the dataset size for demo purposes
    train_set = Subset(train_set, indices=list(range(100)))
    val_set = MNIST(download=False, root=path, transform=val_transform, train=False)
    # Reduce the dataset size for demo purposes
    val_set = Subset(val_set, indices=list(range(100)))

    train_loader = DataLoader(train_set, batch_size=train_batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=val_batch_size, shuffle=False)
    return train_loader, val_loader
