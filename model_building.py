import pandas as pd
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
from pytorch_lightning.callbacks import EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
#TODO: Lots of issues here. Think I need to completely rethink my model. I think part of this may be the issue of group
# numbers not increasing like traditional numbers, same for states. Might be looking more towards classification than I
# had originally thought.
import pytorch_lightning as pl


def tensor_description(tensor):
    print(f"Shape of tensor: {tensor.shape}")
    print(f"Datatype of tensor: {tensor.dtype}")
    print(f"Device tensor is stored on: {tensor.device}")


class DMFDataset(Dataset):
    def __init__(self, np_file):
        self.np_file = np_file
        self.tabular = np.load(np_file, allow_pickle=True)
        x2 = self.tabular[:, 7]
        lookupTable, indexed_dataSet = np.unique(x2, return_inverse=True)
        self.tabular[:, 7] = indexed_dataSet
        self.lookupTable = lookupTable
        print(lookupTable)

    def __len__(self):
        return len(self.tabular)

    def __getitem__(self, idx):
        tabular = torch.FloatTensor(self.tabular[idx, (4,5,6,7)].astype(float))
        y = torch.FloatTensor(self.tabular[idx, (1,2)].astype(float))
        return tabular, y


class LitClassifier(pl.LightningModule):
    def __init__(
            self, lr: float = 1e-3, num_workers: int = 8, batch_size: int = 32,
    ):
        super().__init__()
        self.lr = lr
        self.num_workers = num_workers
        self.batch_size = batch_size

        self.ln1 = nn.Linear(4, 10)
        self.ln2 = nn.Linear(10, 10)
        self.ln3 = nn.Linear(10, 2)
        self.relu = nn.ReLU()
    def forward(self, tab):
        tab = self.ln1(tab)
        tab = self.relu(tab)
        tab = self.ln2(tab)
        tab = self.relu(tab)
        return self.ln3(tab)

    def training_step(self, batch, batch_idx):
        tabular, y = batch
        criterion = torch.nn.L1Loss()
        y_pred = self(tabular).double()
        y = y.double()
        #print("Training Step")
        #tensor_description(y_pred)
        #tensor_description(y)
        loss = criterion(y_pred, y)

        tensorboard_logs = {"train_loss": loss}
        return {"loss": loss, "log": tensorboard_logs}

    def validation_step(self, batch, batch_idx):
        tabular, y = batch
        criterion = torch.nn.L1Loss()
        y_pred = self(tabular).double()
        y = y.double()
        #print("Validaton Step")
        #tensor_description(y_pred)
        #tensor_description(y)
        val_loss = criterion(y_pred, y)

        return {"val_loss": val_loss}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x["val_loss"] for x in outputs]).mean()
        tensorboard_logs = {"val_loss": avg_loss}
        return {"val_loss": avg_loss, "log": tensorboard_logs}

    def test_step(self, batch, batch_idx):
        tabular, y = batch

        criterion = torch.nn.L1Loss()
        y_pred = self(tabular).double()
        y = y.double()
        #print("Test Step")
        #tensor_description(y_pred)
        #tensor_description(y)

        test_loss = criterion(y_pred, y)

        return {"test_loss": test_loss}

    def test_epoch_end(self, outputs):
        avg_loss = torch.stack([x["test_loss"] for x in outputs]).mean()
        logs = {"test_loss": avg_loss}
        return {"test_loss": avg_loss, "log": logs, "progress_bar": logs}

    def setup(self, stage):
        dmf_data = DMFDataset("Death-Master-File-Data/formatted_data.npy")

        train_size = int(0.80 * len(dmf_data))
        val_size = int((len(dmf_data) - train_size) / 2)
        test_size = len(dmf_data)-train_size-val_size

        self.train_set, self.val_set, self.test_set = random_split(dmf_data, (train_size, val_size, test_size))

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=(self.lr))

    def train_dataloader(self):
        return DataLoader(self.train_set, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.val_set, batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.test_set, batch_size=self.batch_size)


if __name__ == "__main__":
    logger = TensorBoardLogger("lightning_logs", name="multi_input")
    early_stop_callback = EarlyStopping(monitor="val_loss", min_delta=20, patience=3, verbose=False, mode="min")

    model = LitClassifier()
    trainer = pl.Trainer(logger=logger, max_epochs=10)

    lr_finder = trainer.tuner.lr_find(model)
    fig = lr_finder.plot(suggest=True, show=True)
    new_lr = lr_finder.suggestion()
    model.hparams.lr = new_lr

    trainer.fit(model)
    trainer.test(model)
    torch.save(model.state_dict(), "model1")
