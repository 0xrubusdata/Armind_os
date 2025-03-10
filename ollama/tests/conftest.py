import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def test_chat_request():
    """Create a test chat request."""
    return {
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
        "system": "You are a helpful assistant"
    } 