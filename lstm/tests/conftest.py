import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.models.lstm import LSTMModel
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_settings(monkeypatch):
    """Mock settings for testing."""
    monkeypatch.setattr(settings, "MODEL_PATH", "test_models")
    monkeypatch.setattr(settings, "DEFAULT_WINDOW_SIZE", 20)
    return settings

@pytest.fixture
def sample_time_series_data() -> Dict[str, List]:
    """Generate sample time series data for testing."""
    num_points = 200
    # Generate dates
    base_date = datetime.now()
    dates = [(base_date + timedelta(days=i)).strftime("%Y-%m-%d") 
             for i in range(num_points)]
    
    # Generate synthetic price data with trend and seasonality
    t = np.linspace(0, 4*np.pi, num_points)
    trend = 0.1 * t
    seasonality = 2 * np.sin(t)
    noise = np.random.normal(0, 0.5, num_points)
    values = trend + seasonality + noise
    
    # Scale to realistic values
    values = 100 * (1 + values/10)
    
    return {
        "dates": dates,
        "values": values.tolist()
    }

@pytest.fixture
def valid_model_request() -> Dict:
    """Generate a valid model creation request."""
    return {
        "name": "test_model",
        "model_config": {
            "input_size": 1,
            "hidden_layer_size": 32,
            "num_layers": 2,
            "output_size": 1,
            "dropout": 0.2
        }
    }

@pytest.fixture
def valid_training_request(sample_time_series_data) -> Dict:
    """Generate a valid training request."""
    return {
        "data": sample_time_series_data["values"],
        "dates": sample_time_series_data["dates"],
        "config": {
            "window_size": 20,
            "train_split_size": 0.8,
            "batch_size": 32,
            "num_epoch": 2,
            "learning_rate": 0.01
        }
    }

@pytest.fixture
def valid_prediction_request(sample_time_series_data) -> Dict:
    """Generate a valid prediction request."""
    return {
        "data": sample_time_series_data["values"][-30:],
        "dates": sample_time_series_data["dates"][-30:]
    }

@pytest.fixture
def invalid_request_data() -> Dict:
    """Generate invalid request data for testing validation."""
    return {
        "empty_data": {"data": [], "dates": []},
        "mismatched_data": {
            "data": [1.0, 2.0],
            "dates": ["2024-01-01"]
        },
        "invalid_model_config": {
            "name": "test_model",
            "model_config": {
                "input_size": 0,
                "hidden_layer_size": -32
            }
        },
        "invalid_training_config": {
            "data": [1.0, 2.0],
            "dates": ["2024-01-01", "2024-01-02"],
            "config": {
                "window_size": 0,
                "train_split_size": 1.5
            }
        }
    } 