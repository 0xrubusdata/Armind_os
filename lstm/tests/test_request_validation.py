import pytest
from pydantic import ValidationError
from app.models.request.model_request import (
    ModelConfig,
    ModelRequest,
    TrainingConfig,
    TrainingRequest,
    PredictionRequest
)

def test_model_config_validation():
    """Test model configuration validation."""
    # Test valid config
    valid_config = {
        "input_size": 1,
        "hidden_layer_size": 32,
        "num_layers": 2,
        "output_size": 1,
        "dropout": 0.2
    }
    config = ModelConfig(**valid_config)
    assert config.input_size == valid_config["input_size"]
    
    # Test invalid input size
    with pytest.raises(ValidationError) as exc_info:
        ModelConfig(input_size=0, hidden_layer_size=32, num_layers=2)
    assert "input_size must be greater than 0" in str(exc_info.value)
    
    # Test invalid dropout
    with pytest.raises(ValidationError) as exc_info:
        ModelConfig(**{**valid_config, "dropout": 1.5})
    assert "dropout must be between 0 and 1" in str(exc_info.value)

def test_model_request_validation():
    """Test model request validation."""
    # Test valid request
    valid_request = {
        "name": "test_model",
        "model_config": {
            "input_size": 1,
            "hidden_layer_size": 32,
            "num_layers": 2,
            "output_size": 1,
            "dropout": 0.2
        }
    }
    request = ModelRequest(**valid_request)
    assert request.name == valid_request["name"]
    
    # Test invalid name
    with pytest.raises(ValidationError) as exc_info:
        ModelRequest(name="", model_config=valid_request["model_config"])
    assert "name cannot be empty" in str(exc_info.value)

def test_training_config_validation():
    """Test training configuration validation."""
    # Test valid config
    valid_config = {
        "window_size": 20,
        "train_split_size": 0.8,
        "batch_size": 32,
        "num_epoch": 100,
        "learning_rate": 0.01
    }
    config = TrainingConfig(**valid_config)
    assert config.window_size == valid_config["window_size"]
    
    # Test invalid window size
    with pytest.raises(ValidationError) as exc_info:
        TrainingConfig(**{**valid_config, "window_size": 0})
    assert "window_size must be greater than 0" in str(exc_info.value)
    
    # Test invalid train split
    with pytest.raises(ValidationError) as exc_info:
        TrainingConfig(**{**valid_config, "train_split_size": 1.5})
    assert "train_split_size must be between 0 and 1" in str(exc_info.value)

def test_training_request_validation(sample_time_series_data):
    """Test training request validation."""
    # Test valid request
    valid_request = {
        "data": sample_time_series_data["values"],
        "dates": sample_time_series_data["dates"],
        "config": {
            "window_size": 20,
            "train_split_size": 0.8,
            "batch_size": 32,
            "num_epoch": 100,
            "learning_rate": 0.01
        }
    }
    request = TrainingRequest(**valid_request)
    assert len(request.data) == len(request.dates)
    
    # Test mismatched lengths
    with pytest.raises(ValidationError) as exc_info:
        TrainingRequest(
            data=sample_time_series_data["values"][:-1],
            dates=sample_time_series_data["dates"],
            config=valid_request["config"]
        )
    assert "data and dates must have the same length" in str(exc_info.value)

def test_prediction_request_validation(sample_time_series_data):
    """Test prediction request validation."""
    # Test valid request
    valid_request = {
        "data": sample_time_series_data["values"][-30:],
        "dates": sample_time_series_data["dates"][-30:]
    }
    request = PredictionRequest(**valid_request)
    assert len(request.data) == len(request.dates)
    
    # Test empty data
    with pytest.raises(ValidationError) as exc_info:
        PredictionRequest(data=[], dates=[])
    assert "data cannot be empty" in str(exc_info.value) 