import pytest
from fastapi.testclient import TestClient

def test_chat_endpoint(client: TestClient, test_chat_request):
    """Test the chat endpoint."""
    response = client.post("/api/v1/chat", json=test_chat_request)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

def test_chat_stream_endpoint(client: TestClient, test_chat_request):
    """Test the chat stream endpoint."""
    response = client.post("/api/v1/chat/stream", json=test_chat_request)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data 