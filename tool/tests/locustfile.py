from locust import HttpUser, task, between
import numpy as np
import json
from datetime import datetime, timedelta

class TalibAPIUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Initialize test data on startup."""
        # Generate sample price data
        num_points = 100
        base_price = 100.0
        trend = np.random.normal(0.0001, 0.0002, num_points).cumsum()
        volatility = np.random.normal(0, 0.02, num_points)
        
        prices = base_price * np.exp(trend + volatility)
        
        self.test_data = {
            "momentum": {
                "real": prices.tolist(),
                "timeperiod": 14,
                "fastperiod": 12,
                "slowperiod": 26,
                "signalperiod": 9
            },
            "volatility": {
                "high": (prices * (1 + abs(np.random.normal(0, 0.01, num_points)))).tolist(),
                "low": (prices * (1 - abs(np.random.normal(0, 0.01, num_points)))).tolist(),
                "close": prices.tolist(),
                "timeperiod": 14
            },
            "volume": {
                "real": prices.tolist(),
                "volume": (np.random.lognormal(10, 1, num_points) * 1000).tolist()
            }
        }
    
    @task(3)
    def test_momentum_indicators(self):
        """Load test momentum indicators."""
        # Test RSI
        with self.client.post(
            "/api/v1/momentum/RSI",
            json={"real": self.test_data["momentum"]["real"], "timeperiod": 14},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"RSI failed with status {response.status_code}")
        
        # Test MACD
        with self.client.post(
            "/api/v1/momentum/MACD",
            json=self.test_data["momentum"],
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"MACD failed with status {response.status_code}")
    
    @task(2)
    def test_volatility_indicators(self):
        """Load test volatility indicators."""
        # Test ATR
        with self.client.post(
            "/api/v1/volatility/ATR",
            json=self.test_data["volatility"],
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"ATR failed with status {response.status_code}")
    
    @task(1)
    def test_volume_indicators(self):
        """Load test volume indicators."""
        # Test OBV
        with self.client.post(
            "/api/v1/volume/OBV",
            json=self.test_data["volume"],
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"OBV failed with status {response.status_code}")
    
    @task(1)
    def test_error_cases(self):
        """Load test error handling."""
        # Test invalid data
        with self.client.post(
            "/api/v1/momentum/RSI",
            json={"real": []},
            catch_response=True
        ) as response:
            if response.status_code == 422:
                response.success()
            else:
                response.failure(f"Error case failed with status {response.status_code}")
        
        # Test invalid function
        with self.client.post(
            "/api/v1/momentum/INVALID_FUNC",
            json=self.test_data["momentum"],
            catch_response=True
        ) as response:
            if response.status_code == 404:
                response.success()
            else:
                response.failure(f"Error case failed with status {response.status_code}")
    
    @task(1)
    def test_health_check(self):
        """Load test health check endpoint."""
        with self.client.get(
            "/health",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed with status {response.status_code}") 