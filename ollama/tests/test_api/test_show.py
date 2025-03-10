import pytest
from fastapi.testclient import TestClient

def test_show_endpoint(client: TestClient):
    """Test the show endpoint."""
    response = client.get("/api/v1/show")
    assert response.status_code == 200
    data = response.json()
    assert "model" in data
    assert "details" in data

def test_show_endpoint_model_details(client: TestClient):
    """Test the show endpoint returns model details."""
    response = client.get("/api/v1/show")
    assert response.status_code == 200
    data = response.json()
    details = data["details"]
    assert isinstance(details, dict)
    assert "format" in details
    assert "family" in details 