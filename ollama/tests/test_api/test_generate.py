import pytest
from fastapi.testclient import TestClient
from app.models.request.generate_request import GenerateRequest

@pytest.fixture
def test_generate_request():
    """Create a test generate request."""
    return {
        "prompt": "Write a story about a robot",
        "system": "You are a creative storyteller",
        "template": None,
        "context": None,
        "options": None
    }

def test_generate_endpoint(client: TestClient, test_generate_request):
    """Test the generate endpoint."""
    response = client.post("/api/v1/generate", json=test_generate_request)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "prompt" in data
    assert data["prompt"] == test_generate_request["prompt"]

def test_generate_stream_endpoint(client: TestClient, test_generate_request):
    """Test the generate stream endpoint."""
    response = client.post("/api/v1/generate/stream", json=test_generate_request)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "prompt" in data
    assert data["prompt"] == test_generate_request["prompt"]

def test_generate_with_invalid_request(client: TestClient):
    """Test the generate endpoint with invalid request."""
    invalid_request = {}
    response = client.post("/api/v1/generate", json=invalid_request)
    assert response.status_code == 422  # Validation error

def test_generate_with_system_message(client: TestClient, test_generate_request):
    """Test the generate endpoint with system message."""
    response = client.post("/api/v1/generate", json=test_generate_request)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data 