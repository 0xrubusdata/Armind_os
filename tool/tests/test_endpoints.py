import pytest
from fastapi.testclient import TestClient
from app.core.config import settings

def test_root_endpoint(test_client: TestClient):
    """Test the root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert "Welcome to Armind_OS" in response.json()["message"]

def test_health_check(test_client: TestClient):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_momentum_endpoints(test_client: TestClient, valid_momentum_request):
    """Test momentum indicator endpoints."""
    # Test RSI calculation
    response = test_client.post(
        f"{settings.API_V1_STR}/momentum/RSI",
        json=valid_momentum_request
    )
    assert response.status_code == 200
    assert "results" in response.json()
    assert "real" in response.json()["results"]
    
    # Test MACD calculation
    macd_request = valid_momentum_request.copy()
    macd_request.update({
        "fastperiod": 12,
        "slowperiod": 26,
        "signalperiod": 9
    })
    response = test_client.post(
        f"{settings.API_V1_STR}/momentum/MACD",
        json=macd_request
    )
    assert response.status_code == 200
    assert "results" in response.json()
    assert all(k in response.json()["results"] for k in ["macd", "macdsignal", "macdhist"])

def test_volatility_endpoints(test_client: TestClient, valid_volatility_request):
    """Test volatility indicator endpoints."""
    # Test ATR calculation
    response = test_client.post(
        f"{settings.API_V1_STR}/volatility/ATR",
        json=valid_volatility_request
    )
    assert response.status_code == 200
    assert "results" in response.json()
    assert "real" in response.json()["results"]
    
    # Test NATR calculation
    response = test_client.post(
        f"{settings.API_V1_STR}/volatility/NATR",
        json=valid_volatility_request
    )
    assert response.status_code == 200
    assert "results" in response.json()
    assert "real" in response.json()["results"]

def test_volume_endpoints(test_client: TestClient, valid_volume_request):
    """Test volume indicator endpoints."""
    # Test OBV calculation
    response = test_client.post(
        f"{settings.API_V1_STR}/volume/OBV",
        json=valid_volume_request
    )
    assert response.status_code == 200
    assert "results" in response.json()
    assert "real" in response.json()["results"]

def test_error_handling(test_client: TestClient, invalid_request_data):
    """Test error handling in endpoints."""
    # Test validation error
    response = test_client.post(
        f"{settings.API_V1_STR}/momentum/RSI",
        json=invalid_request_data["empty_data"]
    )
    assert response.status_code == 422
    assert "error_code" in response.json()
    assert response.json()["error_code"] == "VALIDATION_ERROR"
    
    # Test invalid function
    response = test_client.post(
        f"{settings.API_V1_STR}/momentum/INVALID_FUNC",
        json=valid_momentum_request
    )
    assert response.status_code == 404
    assert "error_code" in response.json()
    assert response.json()["error_code"] == "FUNCTION_NOT_FOUND"

def test_rate_limiting(test_client: TestClient, valid_momentum_request):
    """Test rate limiting middleware."""
    # Make requests up to the limit
    for _ in range(settings.RATE_LIMIT_PER_MINUTE):
        response = test_client.post(
            f"{settings.API_V1_STR}/momentum/RSI",
            json=valid_momentum_request
        )
        assert response.status_code == 200
        
        # Check rate limit headers
        assert "X-RateLimit-Limit-Minute" in response.headers
        assert "X-RateLimit-Remaining-Minute" in response.headers
    
    # Next request should be rate limited
    response = test_client.post(
        f"{settings.API_V1_STR}/momentum/RSI",
        json=valid_momentum_request
    )
    assert response.status_code == 429
    assert "error_code" in response.json()
    assert response.json()["error_code"] == "RATE_LIMIT_EXCEEDED" 