import torch
import torch.nn as nn
from typing import Dict, Any, Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class LSTMModel(nn.Module):
    """LSTM model for time series prediction."""
    
    def __init__(self, 
                 input_size: int = settings.DEFAULT_MODEL_CONFIG["input_size"],
                 hidden_layer_size: int = settings.DEFAULT_MODEL_CONFIG["lstm_size"],
                 num_layers: int = settings.DEFAULT_MODEL_CONFIG["num_lstm_layers"],
                 output_size: int = 1,
                 dropout: float = settings.DEFAULT_MODEL_CONFIG["dropout"]):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        self.num_layers = num_layers
        
        self.linear_1 = nn.Linear(input_size, hidden_layer_size)
        self.relu = nn.ReLU()
        self.lstm = nn.LSTM(hidden_layer_size, 
                           hidden_size=self.hidden_layer_size,
                           num_layers=num_layers,
                           batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.linear_2 = nn.Linear(num_layers * hidden_layer_size, output_size)
        
        self.init_weights()
    
    def init_weights(self):
        """Initialize model weights."""
        for name, param in self.lstm.named_parameters():
            if 'bias' in name:
                nn.init.constant_(param, 0.0)
            elif 'weight_ih' in name:
                nn.init.kaiming_normal_(param)
            elif 'weight_hh' in name:
                nn.init.orthogonal_(param)
    
    def forward(self, x):
        """Forward pass."""
        batchsize = x.shape[0]
        
        x = self.linear_1(x)
        x = self.relu(x)
        
        lstm_out, (h_n, c_n) = self.lstm(x)
        
        x = h_n.permute(1, 0, 2).reshape(batchsize, -1)
        
        x = self.dropout(x)
        predictions = self.linear_2(x)
        return predictions[:, -1]
    
    def get_config(self) -> Dict[str, Any]:
        """Get model configuration."""
        return {
            "input_size": self.linear_1.in_features,
            "hidden_layer_size": self.hidden_layer_size,
            "num_layers": self.num_layers,
            "output_size": self.linear_2.out_features,
            "dropout": self.dropout.p
        }
    
    def save(self, path: str):
        """Save model to disk."""
        try:
            torch.save({
                'model_state_dict': self.state_dict(),
                'config': self.get_config()
            }, path)
            logger.info(f"Model saved to {path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise
    
    @classmethod
    def load(cls, path: str) -> 'LSTMModel':
        """Load model from disk."""
        try:
            checkpoint = torch.load(path)
            config = checkpoint['config']
            model = cls(**config)
            model.load_state_dict(checkpoint['model_state_dict'])
            logger.info(f"Model loaded from {path}")
            return model
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise 