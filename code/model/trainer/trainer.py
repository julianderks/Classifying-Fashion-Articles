import torch
from base import BaseTrainer
from tqdm import tqdm


class Trainer(BaseTrainer):
    """
    Trainer class
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

        super().__init__(
            model,
            criterion,
            optimizer,
            config,
            device,
            train_data_loader,
            valid_data_loader,
            metric_funcs,
        )

    def _train_epoch(self, epoch):
        """
        Training logic for an epoch

        :param epoch: Integer, current training epoch.
        :return: A log that contains average loss and metric in this epoch.
        """
        self.model.train()
        self.train_metrics.reset()

        # import iterator bar
        for batch_idx, (data, target) in enumerate(tqdm(self.train_data_loader)):

            data, target = data.to(self.device), target.to(self.device)

            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)
            loss.backward()
            self.optimizer.step()

            self.train_metrics.update("loss", loss.item())
            for met in self.metric_funcs:
                self.train_metrics.update(met.__name__, met(output, target))

        log = self.train_metrics.result()

        if self.do_validation:
            val_log = self._valid_epoch(epoch)
            log.update(**{"val_" + k: v for k, v in val_log.items()})

        return log

    def _valid_epoch(self, epoch):
        """
        Validate after training an epoch

        :param epoch: Integer, current training epoch.
        :return: A log that contains information about validation
        """
        self.model.eval()
        self.valid_metrics.reset()

        with torch.no_grad():
            for batch_idx, (data, target) in enumerate(tqdm(self.valid_data_loader)):
                data, target = data.to(self.device), target.to(self.device)

                output = self.model(data)
                loss = self.criterion(output, target)

                self.valid_metrics.update("loss", loss.item())
                for met in self.metric_funcs:
                    self.valid_metrics.update(met.__name__, met(output, target))

        return loss
