import numpy as np


def get_mnist_data_loaders(train_transform, train_batch_size, val_transform, val_batch_size):

    from torch.utils.data import DataLoader
    from torchvision.datasets import MNIST

    train_loader = DataLoader(
        MNIST(download=True, root=".", transform=train_transform, train=True), batch_size=train_batch_size, shuffle=True
    )

    val_loader = DataLoader(
        MNIST(download=False, root=".", transform=val_transform, train=False), batch_size=val_batch_size, shuffle=False
    )
    return train_loader, val_loader


def get_model(n, m):
    # Dumb model definition
    class Model:
        def __init__(self, n, m):
            self.weights = np.random.randn(n, m)
            self.bias = np.random.randn(n)

        def __call__(self, x):
            return x @ self.weights.transpose() + self.bias

    model = Model(n, m)
    return model
