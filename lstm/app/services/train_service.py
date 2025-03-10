from typing import Dict, Any, Tuple
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import logging
from torch.utils.data import DataLoader

from app.services.base_service import BaseService
from app.models.dataset import prepare_data, Normalizer
from app.models.request.model_request import TrainingRequest, TrainingConfig
from app.core.exceptions import TrainingError

logger = logging.getLogger(__name__)

class TrainingService(BaseService):
    """Service for training LSTM models."""
    
    def train_model(self, model_name: str, request: TrainingRequest) -> Dict[str, Any]:
        """Train a model with the provided data."""
        try:
            # Get model
            model = self.get_model(model_name)
            model.to(self.device)
            
            # Prepare data
            train_loader, val_loader, normalizer = prepare_data(
                np.array(request.data),
                window_size=request.config.get("window_size", 20) if request.config else 20,
                train_split=request.config.get("train_split", 0.8) if request.config else 0.8
            )
            
            # Train model
            train_loss, val_loss = self._train(
                model,
                train_loader,
                val_loader,
                request.config
            )
            
            # Save model
            self.save_model(model_name, model)
            
            return {
                "model_name": model_name,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "epochs": request.config.get("num_epoch", 100) if request.config else 100,
                "message": "Model trained successfully"
            }
        
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise TrainingError(f"Failed to train model: {str(e)}")
    
    def _train(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        config: Dict[str, Any] = None
    ) -> Tuple[float, float]:
        """Train the model."""
        try:
            # Training setup
            criterion = nn.MSELoss()
            optimizer = optim.Adam(
                model.parameters(),
                lr=config.get("learning_rate", 0.01) if config else 0.01
            )
            scheduler = optim.lr_scheduler.StepLR(
                optimizer,
                step_size=config.get("scheduler_step_size", 40) if config else 40,
                gamma=0.1
            )
            
            num_epochs = config.get("num_epoch", 100) if config else 100
            best_val_loss = float('inf')
            
            for epoch in range(num_epochs):
                # Training phase
                model.train()
                train_loss = 0
                for x_batch, y_batch in train_loader:
                    x_batch = x_batch.to(self.device)
                    y_batch = y_batch.to(self.device)
                    
                    optimizer.zero_grad()
                    y_pred = model(x_batch)
                    loss = criterion(y_pred, y_batch)
                    loss.backward()
                    optimizer.step()
                    
                    train_loss += loss.item()
                
                # Validation phase
                model.eval()
                val_loss = 0
                with torch.no_grad():
                    for x_batch, y_batch in val_loader:
                        x_batch = x_batch.to(self.device)
                        y_batch = y_batch.to(self.device)
                        
                        y_pred = model(x_batch)
                        loss = criterion(y_pred, y_batch)
                        val_loss += loss.item()
                
                # Update learning rate
                scheduler.step()
                
                # Log progress
                if (epoch + 1) % 10 == 0:
                    logger.info(
                        f"Epoch [{epoch+1}/{num_epochs}], "
                        f"Train Loss: {train_loss/len(train_loader):.4f}, "
                        f"Val Loss: {val_loss/len(val_loader):.4f}"
                    )
                
                # Save best model
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
            
            return train_loss/len(train_loader), val_loss/len(val_loader)
        
        except Exception as e:
            logger.error(f"Error in training loop: {str(e)}")
            raise TrainingError(f"Training failed: {str(e)}") 