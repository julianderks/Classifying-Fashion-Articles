""" Main training script """
import argparse
import torch

from torch.utils.data import DataLoader

from data.dataset import ImageDataset

import model.loss as module_loss
import model.metric as module_metric
import model.model as module_arch
from config.parse_config import ConfigParser
from trainer import Trainer
from utils import prepare_device


# fix random seeds for reproducibility
# SEED = 123
# torch.manual_seed(SEED)
# torch.backends.cudnn.deterministic = True
# torch.backends.cudnn.benchmark = False
# np.random.seed(SEED)


def main(config):
    logger = config.get_logger("train")

    # setup data_loader instances
    train_data_path = "..\data\data"
    train_dataset = ImageDataset(train_data_path)
    data_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)

    # build model architecture, then print to console
    model = config.init_obj("arch", module_arch)
    logger.info(str(model) + "\n")

    # prepare for (multi-device) GPU training
    device, device_ids = prepare_device(config["n_gpu"], logger)
    model = model.to(device)

    if len(device_ids) > 1:
        model = torch.nn.DataParallel(model, device_ids=device_ids)

    # get function handles of loss and metrics
    criterion = getattr(module_loss, config["loss"])
    metric_funcs = [getattr(module_metric, met) for met in config["metrics"]]
    optimizer = config.init_obj("optimizer", torch.optim, model.parameters())

    trainer = Trainer(
        model,
        criterion,
        optimizer,
        config,
        device,
        data_loader,
        metric_funcs=metric_funcs,
    )
    trainer.train()


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="PyTorch Template")

    args.add_argument(
        "-c",
        "--config",
        default=".\config\config.json",
        type=str,
        help="config file path (default: None)",
    )

    args.add_argument(
        "-r",
        "--resume",
        default=None,
        type=str,
        help="path to latest checkpoint (default: None)",
    )

    args.add_argument(
        "-d",
        "--device",
        default=None,
        type=str,
        help="indices of GPUs to enable (default: all)",
    )

    config = ConfigParser.from_args(args)
    main(config)
