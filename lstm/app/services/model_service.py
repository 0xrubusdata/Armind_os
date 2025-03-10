from typing import Dict, Any, List
import logging

from app.services.base_service import BaseService
from app.models.lstm import LSTMModel
from app.models.request.model_request import ModelRequest, ModelConfig
from app.core.exceptions import LSTMError

logger = logging.getLogger(__name__)

class ModelService(BaseService):
    """Service for managing LSTM models."""
    
    def create_model(self, request: ModelRequest) -> Dict[str, Any]:
        """Create a new LSTM model."""
        try:
            if request.name in self.models:
                raise LSTMError(f"Model {request.name} already exists")
            
            # Create model with specified configuration
            model_config = request.model_config or ModelConfig()
            model = LSTMModel(
                input_size=model_config.input_size,
                hidden_layer_size=model_config.hidden_layer_size,
                num_layers=model_config.num_layers,
                output_size=model_config.output_size,
                dropout=model_config.dropout
            )
            
            # Save model
            self.save_model(request.name, model)
            
            return {
                "name": request.name,
                "config": model.get_config(),
                "status": "created",
                "message": "Model created successfully"
            }
        except Exception as e:
            logger.error(f"Error creating model: {str(e)}")
            raise LSTMError(f"Failed to create model: {str(e)}")
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get model information."""
        try:
            model = self.get_model(model_name)
            return {
                "name": model_name,
                "config": model.get_config(),
                "status": "loaded",
                "message": "Model information retrieved successfully"
            }
        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            raise
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List all available models."""
        try:
            models_info = []
            # List models in memory
            for name, model in self.models.items():
                models_info.append({
                    "name": name,
                    "config": model.get_config(),
                    "status": "loaded"
                })
            
            # List models on disk
            for model_path in self.model_dir.glob("*.pth"):
                name = model_path.stem
                if name not in self.models:
                    models_info.append({
                        "name": name,
                        "status": "saved"
                    })
            
            return models_info
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            raise LSTMError(f"Failed to list models: {str(e)}") 