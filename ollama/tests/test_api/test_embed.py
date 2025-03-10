import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def test_embed_request():
    """Create a test embed request."""
    return {
        "input": "Hello, world!",
        "options": None,
        "system": None
    }

def test_embed_endpoint(client: TestClient, test_embed_request):
    """Test the embed endpoint."""
    response = client.post("/api/v1/embed", json=test_embed_request)
    assert response.status_code == 200
    data = response.json()
    assert "embeddings" in data
    assert "dimensions" in data
    assert isinstance(data["embeddings"], list)
    assert isinstance(data["dimensions"], int)

def test_embed_endpoint_with_invalid_request(client: TestClient):
    """Test the embed endpoint with invalid request."""
    invalid_request = {}
    response = client.post("/api/v1/embed", json=invalid_request)
    assert response.status_code == 422  # Validation error

def test_embed_endpoint_with_list_input(client: TestClient):
    """Test the embed endpoint with list input."""
    request = {
        "input": ["Hello, world!", "Another text"],
        "options": None,
        "system": None
    }
    response = client.post("/api/v1/embed", json=request)
    assert response.status_code == 200
    data = response.json()
    assert "embeddings" in data
    assert isinstance(data["embeddings"], list) 