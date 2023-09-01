
import torch
from torch import nn
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torchvision import models

import lightning as pl

import torchmetrics

class OctaneClassifier(pl.LightningModule):
    """Classification model based on ResNet50 weights, trained with transfer learning method
    """
    def __init__(self):
        super().__init__()
        num_classes = 4
        self.feature_extractor = models.resnet50(weights='DEFAULT')
        
        for param in self.feature_extractor.parameters():
            param.requires_grad = False

        self.classifier = nn.Sequential(
            nn.Linear(1000, 512, bias=True),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            
            nn.Linear(512, 256, bias=True),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            
            nn.Linear(256, 128, bias=True),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            
            nn.Linear(128, num_classes, bias=True)
        )
        
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        
        self.criterion = nn.CrossEntropyLoss()
        
        self.accuracy = torchmetrics.Accuracy(task='multiclass', num_classes=num_classes)
        
        self.train_loss_epoch = []
        self.train_accuracy_epoch = []
        self.val_loss_epoch = []
        self.val_accuracy_epoch = []
        
        self.save_hyperparameters()
        
    def forward(self, x):
        x = self.relu(self.feature_extractor(x))
        x = self.sigmoid(self.classifier(x))
        return x
    
    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        scheduler = {
            'scheduler': ReduceLROnPlateau(
                optimizer=optimizer,
                mode='min',
                factor=0.5,
                patience=3,
                min_lr=1e-8
            ),
            'interval': 'epoch',
            'frequency': 1,
            'reduce_on_plateau': True,
            'monitor': 'val_accuracy_epoch'
        }
        return [optimizer], [scheduler]
    
    def training_step(self, batch, batch_idx, mode='train'):
        x, y = batch
        y_probs = self(x)
        loss = self.criterion(y_probs, y)
        acc = self.accuracy(y_probs, y)
        
        self.log('train_accuracy_step', acc, prog_bar=False, logger=True)
        self.log('train_loss_epoch', loss, prog_bar=False, logger=True)
        
        self.train_accuracy_epoch.append(acc.detach())
        self.train_loss_epoch.append(loss.detach())
        
        return loss
    
    def on_train_epoch_end(self) -> None:
        acc = torch.stack(self.train_accuracy_epoch).mean()
        loss = torch.stack(self.train_loss_epoch).mean()
        
        self.log('train_accuracy_epoch', acc, prog_bar=True, on_epoch=True, logger=True)
        self.log('train_loss_epoch', loss, on_epoch=True, prog_bar=True, logger=True)
        
        self.train_accuracy_epoch.clear()
        self.train_loss_epoch.clear()
        
    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_probs = self(x)
        loss = self.criterion(y_probs, y)
        acc = self.accuracy(y_probs, y)
        
        self.log('val_accuracy_epoch', acc, prog_bar=False, logger=True)
        self.log('val_loss_epoch', loss, prog_bar=False, logger=True)
        
        self.val_accuracy_epoch.append(acc.detach())
        self.val_loss_epoch.append(loss.detach())
        
        return loss
    
    def on_validation_epoch_end(self):
        acc = torch.stack(self.val_accuracy_epoch).mean()
        loss = torch.stack(self.val_loss_epoch).mean()
        
        self.log('val_accuracy_epoch', acc, prog_bar=True, on_epoch=True, logger=True)
        self.log('val_loss_epoch', loss, on_epoch=True, prog_bar=True, logger=True)
        
        self.val_accuracy_epoch.clear()
        self.val_loss_epoch.clear()