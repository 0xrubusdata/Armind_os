from pydantic_settings import BaseSettings
from typing import Dict, Any, Optional
import torch

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LSTM API"
    
    # Default model settings
    DEFAULT_MODEL_CONFIG: Dict[str, Any] = {
        "input_size": 1,
        "num_lstm_layers": 2,
        "lstm_size": 32,
        "dropout": 0.2,
    }
    
    # Default training settings
    DEFAULT_TRAINING_CONFIG: Dict[str, Any] = {
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "batch_size": 64,
        "num_epoch": 100,
        "learning_rate": 0.01,
        "scheduler_step_size": 40,
    }
    
    # Default data settings
    DEFAULT_DATA_CONFIG: Dict[str, Any] = {
        "window_size": 20,
        "train_split_size": 0.80,
    }
    
    # Alpha Vantage settings
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    
    # Plot settings
    PLOT_CONFIG: Dict[str, Any] = {
        "xticks_interval": 90,
        "color_actual": "#001f3f",
        "color_train": "#3D9970",
        "color_val": "#0074D9",
        "color_pred_train": "#3D9970",
        "color_pred_val": "#0074D9",
        "color_pred_test": "#FF4136",
    }
    
    class Config:
        env_file = ".env"

settings = Settings() 