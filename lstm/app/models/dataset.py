import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from typing import Tuple, Optional, List
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class Normalizer:
    """Normalizer for time series data."""
    
    def __init__(self):
        self.mu: Optional[np.ndarray] = None
        self.sd: Optional[np.ndarray] = None
    
    def fit_transform(self, x: np.ndarray) -> np.ndarray:
        """Fit and transform the data."""
        self.mu = np.mean(x, axis=(0), keepdims=True)
        self.sd = np.std(x, axis=(0), keepdims=True)
        return (x - self.mu) / self.sd
    
    def transform(self, x: np.ndarray) -> np.ndarray:
        """Transform the data."""
        if self.mu is None or self.sd is None:
            raise ValueError("Normalizer has not been fitted")
        return (x - self.mu) / self.sd
    
    def inverse_transform(self, x: np.ndarray) -> np.ndarray:
        """Inverse transform the data."""
        if self.mu is None or self.sd is None:
            raise ValueError("Normalizer has not been fitted")
        return (x * self.sd) + self.mu

class TimeSeriesDataset(Dataset):
    """Dataset for time series data."""
    
    def __init__(self, x: np.ndarray, y: np.ndarray):
        """
        Initialize dataset.
        
        Args:
            x: Input features [batch, sequence]
            y: Target values [batch]
        """
        x = np.expand_dims(x, 2)  # [batch, sequence, features]
        self.x = torch.FloatTensor(x)
        self.y = torch.FloatTensor(y)
    
    def __len__(self) -> int:
        return len(self.x)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.x[idx], self.y[idx]

def prepare_data(data: np.ndarray, 
                window_size: int = settings.DEFAULT_DATA_CONFIG["window_size"],
                train_split: float = settings.DEFAULT_DATA_CONFIG["train_split_size"]
                ) -> Tuple[DataLoader, DataLoader, Normalizer]:
    """
    Prepare data for training and validation.
    
    Args:
        data: Time series data
        window_size: Size of the sliding window
        train_split: Ratio of training data
    
    Returns:
        train_loader: DataLoader for training data
        val_loader: DataLoader for validation data
        normalizer: Fitted normalizer
    """
    try:
        # Normalize data
        normalizer = Normalizer()
        normalized_data = normalizer.fit_transform(data)
        
        # Create sequences
        x, x_unseen = create_sequences(normalized_data, window_size)
        y = normalized_data[window_size:]
        
        # Split data
        split_idx = int(len(y) * train_split)
        x_train, x_val = x[:split_idx], x[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Create datasets
        train_dataset = TimeSeriesDataset(x_train, y_train)
        val_dataset = TimeSeriesDataset(x_val, y_val)
        
        # Create dataloaders
        train_loader = DataLoader(
            train_dataset,
            batch_size=settings.DEFAULT_TRAINING_CONFIG["batch_size"],
            shuffle=True
        )
        val_loader = DataLoader(
            val_dataset,
            batch_size=settings.DEFAULT_TRAINING_CONFIG["batch_size"],
            shuffle=False
        )
        
        return train_loader, val_loader, normalizer
    
    except Exception as e:
        logger.error(f"Error preparing data: {str(e)}")
        raise

def create_sequences(data: np.ndarray, window_size: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create sequences from time series data.
    
    Args:
        data: Time series data
        window_size: Size of the sliding window
    
    Returns:
        sequences: Sequences for training/validation
        last_sequence: Last sequence for prediction
    """
    n_row = len(data) - window_size + 1
    sequences = np.lib.stride_tricks.as_strided(
        data, 
        shape=(n_row, window_size), 
        strides=(data.strides[0], data.strides[0])
    )
    return sequences[:-1], sequences[-1] 