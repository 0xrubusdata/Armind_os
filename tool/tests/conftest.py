import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import numpy as np
from typing import Dict, List
from faker import Faker

fake = Faker()

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_settings(monkeypatch):
    """Mock settings for testing."""
    monkeypatch.setattr(settings, "RATE_LIMIT_PER_MINUTE", 1000)
    monkeypatch.setattr(settings, "RATE_LIMIT_PER_HOUR", 10000)
    return settings

@pytest.fixture
def sample_price_data() -> Dict[str, List[float]]:
    """Generate sample price data for testing."""
    num_points = 100
    timestamps = [fake.date_time_this_year() for _ in range(num_points)]
    timestamps.sort()  # Ensure chronological order
    
    # Generate realistic price data with trends and volatility
    base_price = 100.0
    trend = np.random.normal(0.0001, 0.0002, num_points).cumsum()
    volatility = np.random.normal(0, 0.02, num_points)
    
    prices = base_price * np.exp(trend + volatility)
    
    return {
        "open": prices.tolist(),
        "high": (prices * (1 + abs(np.random.normal(0, 0.01, num_points)))).tolist(),
        "low": (prices * (1 - abs(np.random.normal(0, 0.01, num_points)))).tolist(),
        "close": (prices * (1 + np.random.normal(0, 0.005, num_points))).tolist(),
        "volume": (np.random.lognormal(10, 1, num_points) * 1000).tolist()
    }

@pytest.fixture
def valid_momentum_request(sample_price_data) -> Dict:
    """Generate a valid momentum request."""
    return {
        "real": sample_price_data["close"],
        "timeperiod": 14
    }

@pytest.fixture
def valid_volatility_request(sample_price_data) -> Dict:
    """Generate a valid volatility request."""
    return {
        "high": sample_price_data["high"],
        "low": sample_price_data["low"],
        "close": sample_price_data["close"],
        "timeperiod": 14
    }

@pytest.fixture
def valid_volume_request(sample_price_data) -> Dict:
    """Generate a valid volume request."""
    return {
        "real": sample_price_data["close"],
        "volume": sample_price_data["volume"]
    }

@pytest.fixture
def invalid_request_data() -> Dict:
    """Generate invalid request data for testing validation."""
    return {
        "empty_data": {"real": []},
        "invalid_timeperiod": {"real": [1.0, 2.0, 3.0], "timeperiod": 0},
        "missing_required": {},
        "invalid_price": {"real": [1.0, "invalid", 3.0]},
        "mismatched_arrays": {
            "high": [1.0, 2.0],
            "low": [0.5],
            "close": [1.5, 2.5]
        }
    } 