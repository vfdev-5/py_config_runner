from typing import Any, Iterable
from py_config_runner import Schema, get_params

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# this config schema can be imported if torch is installed
from py_config_runner import TrainConfigSchema


class TorchTrainingConfigSchema(Schema):
    # Define required parameters for another training config
    # Type hints are from typing
    seed: int
    debug: bool

    num_epochs: int

    train_loader: DataLoader
    val_loader: DataLoader

    model: nn.Module
    criterion: nn.Module
    optimizer: optim.Optimizer


def run(config, **kwargs):
    # Let's validate the config
    TorchTrainingConfigSchema.validate(config)
    # and additionally agains built-in TrainConfigSchema
    TrainConfigSchema.validate(config)

    print("Configuration: ")
    for k, v in get_params(config, TrainConfigSchema).items():
        print(f"\t{k}: {v}")

    device = config.get("device", "cuda")
    model = config.model
    model.to(device)

    criterion = config.criterion
    optimizer = config.optimizer

    for e in range(config.num_epochs):
        print("Epoch {} / {}".format(e + 1, config.num_epochs))
        for i, batch in enumerate(config.train_loader):
            if (i % 50) == 0:
                print(" ", end=".")
            x, y = batch[0].to(device), batch[1].to(device)
            optimizer.zero_grad()
            y_pred = model(x)
            loss = criterion(y_pred, y)
            loss.backward()
            optimizer.step()
        print("")

        if e % config.get("val_interval", 3) == 0:
            num_corrects = 0
            num_samples = 0
            for batch in config.val_loader:
                x, y = batch[0].to(device), batch[1].to(device)
                y_pred = model(x)

                num_corrects += (y_pred.argmax(dim=1) == y).sum()
                num_samples += y_pred.shape[0]

            print(f"Validation: accuracy = {num_corrects / num_samples}")
