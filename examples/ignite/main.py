import argparse
from pathlib import Path

import ignite.distributed as idist
from ignite.engine import create_supervised_evaluator, create_supervised_trainer, Events
from ignite.handlers import ModelCheckpoint
from ignite.metrics import Accuracy, Loss
from ignite.utils import manual_seed, setup_logger
from ignite.contrib.handlers.tensorboard_logger import global_step_from_engine, TensorboardLogger

from py_config_runner import ConfigObject


def training(rank, config):
    rank = idist.get_rank()
    manual_seed(config["seed"] + rank)
    device = idist.device()

    # Define output folder:
    config.output = "/tmp/output"

    model = idist.auto_model(config.model)
    optimizer = idist.auto_optim(config.optimizer)
    criterion = config.criterion

    train_set, val_set = config.train_set, config.val_set
    train_loader = idist.auto_dataloader(train_set, batch_size=config.train_batch_size)
    val_loader = idist.auto_dataloader(val_set, batch_size=config.val_batch_size)

    trainer = create_supervised_trainer(model, optimizer, criterion, device=device)
    trainer.logger = setup_logger("Trainer")

    metrics = {"accuracy": Accuracy(), "loss": Loss(criterion)}

    train_evaluator = create_supervised_evaluator(model, metrics=metrics, device=device)
    train_evaluator.logger = setup_logger("Train Evaluator")
    validation_evaluator = create_supervised_evaluator(model, metrics=metrics, device=device)
    validation_evaluator.logger = setup_logger("Val Evaluator")

    @trainer.on(Events.EPOCH_COMPLETED(every=config.val_interval))
    def compute_metrics(engine):
        train_evaluator.run(train_loader)
        validation_evaluator.run(val_loader)

    if rank == 0:
        tb_logger = TensorboardLogger(log_dir=config.output)

        tb_logger.attach_output_handler(
            trainer,
            event_name=Events.ITERATION_COMPLETED(every=100),
            tag="training",
            output_transform=lambda loss: {"batchloss": loss},
            metric_names="all",
        )

        for tag, evaluator in [("training", train_evaluator), ("validation", validation_evaluator)]:
            tb_logger.attach_output_handler(
                evaluator,
                event_name=Events.EPOCH_COMPLETED,
                tag=tag,
                metric_names=["loss", "accuracy"],
                global_step_transform=global_step_from_engine(trainer),
            )

        tb_logger.attach_opt_params_handler(
            trainer, event_name=Events.ITERATION_COMPLETED(every=100), optimizer=optimizer
        )

    model_checkpoint = ModelCheckpoint(
        config.output,
        n_saved=2,
        filename_prefix="best",
        score_name="accuracy",
        global_step_transform=global_step_from_engine(trainer),
    )
    validation_evaluator.add_event_handler(Events.COMPLETED, model_checkpoint, {"model": model})

    trainer.run(train_loader, max_epochs=config.num_epochs)

    if rank == 0:
        tb_logger.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Example application")
    parser.add_argument("--config", type=Path, help="Input configuration file")
    parser.add_argument("--backend", type=str, default="gloo", help="Distributed backend. Default 'gloo'")
    parser.add_argument("--nproc_per_node", type=int, default=None, help="Number of process to spawn from this script")
    parser.add_argument("--bs", type=int, default=None, help="Override train batch size")
    parser.add_argument("--lr", type=float, default=None, help="Override train learning rate")
    parser.add_argument("--ep", type=int, default=None, help="Override number of epochs")
    args = parser.parse_args()

    assert args.config is not None
    assert args.config.exists()

    # Define configuration mutations if certain cmd args are defined
    mutations = {}
    if args.bs is not None:
        mutations["train_batch_size"] = args.bs
    if args.lr is not None:
        mutations["learning_rate"] = args.lr
    if args.ep is not None:
        mutations["num_epochs"] = args.ep

    # Pass configuration file into py_config_runner.ConfigObject
    # and fetch configuration parameters as attributes
    config = ConfigObject(args.config, mutations=mutations)

    with idist.Parallel(backend=args.backend, nproc_per_node=args.nproc_per_node) as parallel:
        parallel.run(training, config)
