from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.core.config import settings

class ModelConfig(BaseModel):
    """Model configuration."""
    input_size: int = Field(
        default=settings.DEFAULT_MODEL_CONFIG["input_size"],
        description="Input feature size"
    )
    hidden_layer_size: int = Field(
        default=settings.DEFAULT_MODEL_CONFIG["lstm_size"],
        description="Hidden layer size"
    )
    num_layers: int = Field(
        default=settings.DEFAULT_MODEL_CONFIG["num_lstm_layers"],
        description="Number of LSTM layers"
    )
    output_size: int = Field(1, description="Output size")
    dropout: float = Field(
        default=settings.DEFAULT_MODEL_CONFIG["dropout"],
        description="Dropout rate"
    )

class TrainingConfig(BaseModel):
    """Training configuration."""
    batch_size: int = Field(
        default=settings.DEFAULT_TRAINING_CONFIG["batch_size"],
        description="Training batch size"
    )
    num_epoch: int = Field(
        default=settings.DEFAULT_TRAINING_CONFIG["num_epoch"],
        description="Number of training epochs"
    )
    learning_rate: float = Field(
        default=settings.DEFAULT_TRAINING_CONFIG["learning_rate"],
        description="Learning rate"
    )
    scheduler_step_size: int = Field(
        default=settings.DEFAULT_TRAINING_CONFIG["scheduler_step_size"],
        description="Steps before learning rate decay"
    )

class DataConfig(BaseModel):
    """Data configuration."""
    window_size: int = Field(
        default=settings.DEFAULT_DATA_CONFIG["window_size"],
        description="Window size for time series"
    )
    train_split_size: float = Field(
        default=settings.DEFAULT_DATA_CONFIG["train_split_size"],
        description="Training data split ratio"
    )

class ModelRequest(BaseModel):
    """Request for creating a model."""
    name: str = Field(..., description="Model name")
    model_configuration: Optional[ModelConfig] = Field(default_factory=ModelConfig)
    training_configuration: Optional[TrainingConfig] = Field(default_factory=TrainingConfig)
    data_configuration: Optional[DataConfig] = Field(default_factory=DataConfig)

class TrainingRequest(BaseModel):
    """Request for training a model."""
    data: List[float] = Field(..., description="Training data")
    dates: Optional[List[str]] = Field(None, description="Data timestamps")
    symbol: Optional[str] = Field(None, description="Stock symbol")
    configuration: Optional[Dict[str, Any]] = Field(None, description="Additional configuration")

class PredictionRequest(BaseModel):
    """Request for making predictions."""
    data: List[float] = Field(..., description="Input data")
    dates: Optional[List[str]] = Field(None, description="Data timestamps")

class ModelResponse(BaseModel):
    """Response containing model information."""
    name: str
    configuration: Dict[str, Any]
    status: str
    message: Optional[str] = None

class TrainingResponse(BaseModel):
    """Response containing training results."""
    model_name: str
    train_loss: float
    val_loss: float
    epochs: int
    message: str

class PredictionResponse(BaseModel):
    """Response containing predictions."""
    predictions: List[float]
    dates: Optional[List[str]] = None 