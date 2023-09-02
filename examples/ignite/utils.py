from torchvision.datasets import MNIST


def get_mnist_datasets(path, train_transform, val_transform):
    train_set = MNIST(download=True, root=path, transform=train_transform, train=True)
    val_set = MNIST(download=False, root=path, transform=val_transform, train=False)
    return train_set, val_set
