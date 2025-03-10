from locust import HttpUser, task, between
import numpy as np
from datetime import datetime, timedelta
import json

class LSTMAPIUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Initialize test data and create model."""
        # Generate sample time series data
        num_points = 200
        base_date = datetime.now()
        self.dates = [(base_date + timedelta(days=i)).strftime("%Y-%m-%d") 
                     for i in range(num_points)]
        
        t = np.linspace(0, 4*np.pi, num_points)
        trend = 0.1 * t
        seasonality = 2 * np.sin(t)
        noise = np.random.normal(0, 0.5, num_points)
        values = trend + seasonality + noise
        self.values = (100 * (1 + values/10)).tolist()
        
        # Prepare test data
        self.test_data = {
            "model": {
                "name": f"test_model_{self.host}",
                "model_config": {
                    "input_size": 1,
                    "hidden_layer_size": 32,
                    "num_layers": 2,
                    "output_size": 1,
                    "dropout": 0.2
                }
            },
            "training": {
                "data": self.values,
                "dates": self.dates,
                "config": {
                    "window_size": 20,
                    "train_split_size": 0.8,
                    "batch_size": 32,
                    "num_epoch": 2,
                    "learning_rate": 0.01
                }
            },
            "prediction": {
                "data": self.values[-30:],
                "dates": self.dates[-30:]
            }
        }
        
        # Create model
        self.client.post("/api/v1/model/", json=self.test_data["model"])
    
    @task(3)
    def test_model_endpoints(self):
        """Load test model management endpoints."""
        # Get model info
        with self.client.get(
            f"/api/v1/model/{self.test_data['model']['name']}",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Get model failed with status {response.status_code}")
        
        # List models
        with self.client.get(
            "/api/v1/model/",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"List models failed with status {response.status_code}")
    
    @task(2)
    def test_training_endpoint(self):
        """Load test model training endpoint."""
        with self.client.post(
            f"/api/v1/train/{self.test_data['model']['name']}",
            json=self.test_data["training"],
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Training failed with status {response.status_code}")
    
    @task(2)
    def test_prediction_endpoint(self):
        """Load test prediction endpoint."""
        with self.client.post(
            f"/api/v1/evaluate/{self.test_data['model']['name']}/predict",
            json=self.test_data["prediction"],
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Prediction failed with status {response.status_code}")
    
    @task(1)
    def test_evaluation_endpoint(self):
        """Load test evaluation endpoint."""
        with self.client.post(
            f"/api/v1/evaluate/{self.test_data['model']['name']}/evaluate",
            json=self.test_data["prediction"],
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Evaluation failed with status {response.status_code}")
    
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