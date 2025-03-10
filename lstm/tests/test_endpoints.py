import pytest
from fastapi.testclient import TestClient
from app.core.config import settings

def test_root_endpoint(test_client: TestClient):
    """Test the root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert "LSTM API" in response.json()["message"]

def test_health_check(test_client: TestClient):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_model_endpoints(test_client: TestClient, valid_model_request):
    """Test model management endpoints."""
    # Test model creation
    response = test_client.post(
        f"{settings.API_V1_STR}/model/",
        json=valid_model_request
    )
    assert response.status_code == 201
    assert "model_info" in response.json()
    assert response.json()["model_info"]["name"] == valid_model_request["name"]
    
    # Test get model info
    response = test_client.get(
        f"{settings.API_V1_STR}/model/{valid_model_request['name']}"
    )
    assert response.status_code == 200
    assert "model_info" in response.json()
    
    # Test list models
    response = test_client.get(f"{settings.API_V1_STR}/model/")
    assert response.status_code == 200
    assert "models" in response.json()
    assert len(response.json()["models"]) > 0
    
    # Test delete model
    response = test_client.delete(
        f"{settings.API_V1_STR}/model/{valid_model_request['name']}"
    )
    assert response.status_code == 200
    assert "success" in response.json()

def test_training_endpoint(
    test_client: TestClient,
    valid_model_request,
    valid_training_request
):
    """Test model training endpoint."""
    # Create model first
    test_client.post(f"{settings.API_V1_STR}/model/", json=valid_model_request)
    
    # Test training
    response = test_client.post(
        f"{settings.API_V1_STR}/train/{valid_model_request['name']}",
        json=valid_training_request
    )
    assert response.status_code == 200
    assert "training_info" in response.json()
    assert "loss" in response.json()["training_info"]

def test_evaluation_endpoints(
    test_client: TestClient,
    valid_model_request,
    valid_training_request,
    valid_prediction_request
):
    """Test model evaluation endpoints."""
    # Create and train model first
    test_client.post(f"{settings.API_V1_STR}/model/", json=valid_model_request)
    test_client.post(
        f"{settings.API_V1_STR}/train/{valid_model_request['name']}",
        json=valid_training_request
    )
    
    # Test prediction
    response = test_client.post(
        f"{settings.API_V1_STR}/evaluate/{valid_model_request['name']}/predict",
        json=valid_prediction_request
    )
    assert response.status_code == 200
    assert "predictions" in response.json()
    
    # Test evaluation
    response = test_client.post(
        f"{settings.API_V1_STR}/evaluate/{valid_model_request['name']}/evaluate",
        json=valid_prediction_request
    )
    assert response.status_code == 200
    assert "metrics" in response.json()
    assert "mse" in response.json()["metrics"]

def test_error_handling(test_client: TestClient, invalid_request_data):
    """Test error handling in endpoints."""
    # Test validation error
    response = test_client.post(
        f"{settings.API_V1_STR}/model/",
        json=invalid_request_data["invalid_model_config"]
    )
    assert response.status_code == 422
    
    # Test model not found
    response = test_client.get(f"{settings.API_V1_STR}/model/nonexistent_model")
    assert response.status_code == 404
    assert "error" in response.json() 