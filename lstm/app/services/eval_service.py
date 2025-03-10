from typing import Dict, Any, List
import torch
import numpy as np
import logging

from app.services.base_service import BaseService
from app.models.dataset import Normalizer, create_sequences
from app.models.request.model_request import PredictionRequest
from app.core.exceptions import EvaluationError

logger = logging.getLogger(__name__)

class EvaluationService(BaseService):
    """Service for evaluating LSTM models."""
    
    def predict(self, model_name: str, request: PredictionRequest) -> Dict[str, Any]:
        """Make predictions using the model."""
        try:
            # Get model
            model = self.get_model(model_name)
            model.to(self.device)
            model.eval()
            
            # Prepare data
            data = np.array(request.data)
            normalizer = Normalizer()
            normalized_data = normalizer.fit_transform(data)
            
            # Create sequence for prediction
            x, x_unseen = create_sequences(normalized_data, window_size=20)
            x_unseen = torch.FloatTensor(x_unseen).unsqueeze(0).unsqueeze(2).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                prediction = model(x_unseen)
                prediction = prediction.cpu().numpy()
            
            # Inverse transform prediction
            prediction = normalizer.inverse_transform(prediction)
            
            return {
                "predictions": prediction.tolist(),
                "dates": request.dates[-len(prediction):] if request.dates else None
            }
        
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise EvaluationError(f"Prediction failed: {str(e)}")
    
    def evaluate(self, model_name: str, request: PredictionRequest) -> Dict[str, Any]:
        """Evaluate model performance on test data."""
        try:
            # Get model
            model = self.get_model(model_name)
            model.to(self.device)
            model.eval()
            
            # Prepare data
            data = np.array(request.data)
            normalizer = Normalizer()
            normalized_data = normalizer.fit_transform(data)
            
            # Create sequences
            x, _ = create_sequences(normalized_data, window_size=20)
            y = normalized_data[20:]
            
            # Convert to tensors
            x = torch.FloatTensor(x).unsqueeze(2).to(self.device)
            y = torch.FloatTensor(y).to(self.device)
            
            # Make predictions
            with torch.no_grad():
                predictions = model(x)
                mse_loss = torch.nn.MSELoss()(predictions, y)
                mae_loss = torch.nn.L1Loss()(predictions, y)
            
            # Convert predictions back to original scale
            predictions = normalizer.inverse_transform(predictions.cpu().numpy())
            actual = normalizer.inverse_transform(y.cpu().numpy())
            
            return {
                "mse": mse_loss.item(),
                "mae": mae_loss.item(),
                "predictions": predictions.tolist(),
                "actual": actual.tolist(),
                "dates": request.dates[20:] if request.dates else None
            }
        
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            raise EvaluationError(f"Evaluation failed: {str(e)}") 