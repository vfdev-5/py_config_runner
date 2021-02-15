import numpy as np


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
