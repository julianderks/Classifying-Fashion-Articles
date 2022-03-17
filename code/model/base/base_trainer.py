import torch

from utils import MetricTracker


class BaseTrainer:
    """
    Base class for all trainers
    """

    def __init__(
        self,
        model,
        criterion,
        optimizer,
        config,
        device,
        train_data_loader,
        valid_data_loader=None,
        metric_funcs=[],
    ):

        self.config = config
        self.logger = config.get_logger("trainer", config["trainer"]["verbosity"])

        self.device = device

        self.train_data_loader = train_data_loader
        self.valid_data_loader = valid_data_loader
        self.do_validation = self.valid_data_loader is not None

        self.metric_funcs = metric_funcs
        self.train_metrics = MetricTracker("loss", *[m.__name__ for m in metric_funcs])
        self.valid_metrics = MetricTracker("loss", *[m.__name__ for m in metric_funcs])

        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer

        cfg_trainer = config["trainer"]
        self.epochs = cfg_trainer["epochs"]
        self.save_period = cfg_trainer["save_period"]

        self.start_epoch = 1

        self.checkpoint_dir = config.save_dir / "checkpoints"

        if config.resume is not None:
            self._resume_checkpoint(config.resume)

    def _train_epoch(self, epoch):
        """
        Training logic for an epoch

        :param epoch: Current epoch number
        """
        raise NotImplementedError

    def train(self):
        """
        Full training logic
        """

        for epoch in range(self.start_epoch, self.epochs + 1):
            result = self._train_epoch(epoch)

            # save logged informations into log dict
            log = {"epoch": epoch}
            log.update(result)

            # print logged informations to the screen
            for key, value in log.items():
                self.logger.info(f"    {str(key):15s}: {value}")

            best = False  # TO DO save best validation metric model separately
            if epoch % self.save_period == 0:
                self._save_checkpoint(epoch, save_best=best)

    def _save_checkpoint(self, epoch, save_best=False):
        """
        Saving checkpoints

        :param epoch: current epoch number
        :param log: logging information of the epoch
        :param save_best: if True, rename the saved checkpoint to 'model_best.pth'
        """
        arch = type(self.model).__name__
        state = {
            "arch": arch,
            "epoch": epoch,
            "state_dict": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
        }

        filename = str(self.checkpoint_dir / f"checkpoint-epoch{epoch}.pth")
        torch.save(state, filename)
        self.logger.info(f"Saving checkpoint: {filename} ...\n")

        if save_best:
            best_path = str(self.checkpoint_dir / "model_best.pth")
            torch.save(state, best_path)
            self.logger.info("Saving current best: model_best.pth ...")

    def _resume_checkpoint(self, resume_path):
        """
        Resume from saved checkpoints

        :param resume_path: Checkpoint path to be resumed
        """
        resume_path = str(resume_path)

        self.logger.info(f"Loading checkpoint: {resume_path} ...")
        checkpoint = torch.load(resume_path)

        self.start_epoch = checkpoint["epoch"] + 1

        self.model.load_state_dict(checkpoint["state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])

        self.logger.info(
            f"Checkpoint loaded. Resume training from epoch {self.start_epoch}"
        )
