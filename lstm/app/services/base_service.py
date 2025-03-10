from typing import Dict, Any, Optional
import torch
import logging
import os
from pathlib import Path

from app.core.exceptions import ModelNotFoundError, LSTMError
from app.models.lstm import LSTMModel
from app.core.config import settings

logger = logging.getLogger(__name__)

class BaseService:
    """Base service for LSTM operations."""
    
    def __init__(self):
        self.models: Dict[str, LSTMModel] = {}
        self.device = torch.device(settings.DEFAULT_TRAINING_CONFIG["device"])
        self.model_dir = Path("models")
        self.model_dir.mkdir(exist_ok=True)
    
    def get_model(self, model_name: str) -> LSTMModel:
        """Get a model by name."""
        if model_name not in self.models:
            # Try to load from disk
            model_path = self.model_dir / f"{model_name}.pth"
            if model_path.exists():
                self.load_model(model_name)
            else:
                raise ModelNotFoundError(f"Model {model_name} not found")
        return self.models[model_name]
    
    def save_model(self, model_name: str, model: LSTMModel):
        """Save model to disk."""
        try:
            model_path = self.model_dir / f"{model_name}.pth"
            model.save(str(model_path))
            self.models[model_name] = model
        except Exception as e:
            logger.error(f"Error saving model {model_name}: {str(e)}")
            raise LSTMError(f"Failed to save model: {str(e)}")
    
    def load_model(self, model_name: str) -> LSTMModel:
        """Load model from disk."""
        try:
            model_path = self.model_dir / f"{model_name}.pth"
            model = LSTMModel.load(str(model_path))
            model = model.to(self.device)
            self.models[model_name] = model
            return model
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {str(e)}")
            raise LSTMError(f"Failed to load model: {str(e)}")
    
    def delete_model(self, model_name: str):
        """Delete model from memory and disk."""
        try:
            if model_name in self.models:
                del self.models[model_name]
            
            model_path = self.model_dir / f"{model_name}.pth"
            if model_path.exists():
                os.remove(model_path)
        except Exception as e:
            logger.error(f"Error deleting model {model_name}: {str(e)}")
            raise LSTMError(f"Failed to delete model: {str(e)}") 