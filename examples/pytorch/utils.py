from torch.utils.data import DataLoader
from torchvision.datasets import MNIST


def get_mnist_data_loaders(path, train_transform, train_batch_size, val_transform, val_batch_size):

    train_loader = DataLoader(
        MNIST(download=True, root=path, transform=train_transform, train=True),
        batch_size=train_batch_size,
        shuffle=True,
    )

    val_loader = DataLoader(
        MNIST(download=False, root=path, transform=val_transform, train=False), batch_size=val_batch_size, shuffle=False
    )
    return train_loader, val_loader
