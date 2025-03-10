# LSTM Time Series Prediction API

A high-performance REST API for time series prediction using LSTM (Long Short-Term Memory) neural networks. This service provides endpoints for creating, training, and using LSTM models for time series forecasting.

## Features

- **Model Management**: Create, list, retrieve, and delete LSTM models
- **Training**: Train models on time series data with customizable configurations
- **Prediction**: Make predictions using trained models
- **Evaluation**: Evaluate model performance on test data
- **Data Processing**: Built-in data normalization and sequence preparation
- **Persistence**: Models are automatically saved and can be reloaded
- **Async Support**: All operations are asynchronous for better performance

## Installation

### Using Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd lstm
```

2. Build and run the Docker container:
```bash
docker build -t lstm-api .
docker run -d -p 8000:8000 --name lstm-api lstm-api
```

### Local Installation

1. Clone the repository and create a virtual environment:
```bash
git clone <repository-url>
cd lstm
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

The API will be available at `http://localhost:8000`. Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### Model Management

1. Create a new model:
```bash
POST /api/v1/model/
```
```json
{
    "name": "stock_predictor",
    "model_config": {
        "input_size": 1,
        "hidden_layer_size": 32,
        "num_layers": 2,
        "output_size": 1,
        "dropout": 0.2
    }
}
```

2. List all models:
```bash
GET /api/v1/model/
```

3. Get model information:
```bash
GET /api/v1/model/{model_name}
```

4. Delete a model:
```bash
DELETE /api/v1/model/{model_name}
```

#### Training

Train a model:
```bash
POST /api/v1/train/{model_name}
```
```json
{
    "data": [100.0, 101.5, 99.8, 102.3, ...],
    "dates": ["2024-01-01", "2024-01-02", ...],
    "config": {
        "window_size": 20,
        "train_split_size": 0.8,
        "batch_size": 64,
        "num_epoch": 100,
        "learning_rate": 0.01
    }
}
```

#### Evaluation

1. Make predictions:
```bash
POST /api/v1/evaluate/{model_name}/predict
```
```json
{
    "data": [100.0, 101.5, 99.8, 102.3, ...],
    "dates": ["2024-01-01", "2024-01-02", ...]
}
```

2. Evaluate model:
```bash
POST /api/v1/evaluate/{model_name}/evaluate
```
```json
{
    "data": [100.0, 101.5, 99.8, 102.3, ...],
    "dates": ["2024-01-01", "2024-01-02", ...]
}
```

## Usage Examples

### 1. Stock Price Prediction

```python
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

# Create a model
model_config = {
    "name": "stock_predictor",
    "model_config": {
        "input_size": 1,
        "hidden_layer_size": 32,
        "num_layers": 2,
        "dropout": 0.2
    }
}
response = requests.post(f"{BASE_URL}/model/", json=model_config)
print("Model created:", response.json())

# Train the model
training_data = {
    "data": [100.0, 101.5, 99.8, 102.3, ...],  # Your stock prices
    "dates": ["2024-01-01", "2024-01-02", ...], # Corresponding dates
    "config": {
        "window_size": 20,
        "train_split_size": 0.8,
        "num_epoch": 100
    }
}
response = requests.post(
    f"{BASE_URL}/train/stock_predictor",
    json=training_data
)
print("Training results:", response.json())

# Make predictions
prediction_data = {
    "data": [102.3, 103.1, 101.8, ...],  # Recent stock prices
    "dates": ["2024-03-01", "2024-03-02", ...]
}
response = requests.post(
    f"{BASE_URL}/evaluate/stock_predictor/predict",
    json=prediction_data
)
print("Predictions:", response.json())
```

### 2. Time Series Cross-Validation

```python
import numpy as np
import requests

def cross_validate(data, n_splits=5):
    split_size = len(data) // n_splits
    scores = []
    
    for i in range(n_splits - 1):
        # Prepare test data
        test_data = data[i * split_size:(i + 1) * split_size]
        train_data = np.concatenate([
            data[:i * split_size],
            data[(i + 1) * split_size:]
        ])
        
        # Train model
        training_request = {
            "data": train_data.tolist(),
            "config": {"num_epoch": 50}
        }
        requests.post(
            f"{BASE_URL}/train/stock_predictor",
            json=training_request
        )
        
        # Evaluate
        eval_request = {"data": test_data.tolist()}
        response = requests.post(
            f"{BASE_URL}/evaluate/stock_predictor/evaluate",
            json=eval_request
        )
        scores.append(response.json()["mse"])
    
    return np.mean(scores), np.std(scores)
```

## Configuration

The API can be configured using environment variables:

```env
# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=LSTM API

# Model Settings
DEFAULT_WINDOW_SIZE=20
DEFAULT_TRAIN_SPLIT=0.8
DEFAULT_BATCH_SIZE=64
DEFAULT_NUM_EPOCHS=100
```

## Error Handling

The API uses standard HTTP status codes:

- 200: Successful operation
- 201: Resource created
- 400: Bad request (invalid parameters)
- 404: Resource not found
- 500: Internal server error

Errors include detailed messages to help diagnose issues.

---

## 🎨 How to Contribute
We welcome contributions from developers, designers, and visionaries. Feel free to fork this repository, submit issues, or open pull requests.

---

## 📜 License
This project is licensed under the MIT License.

---

## 📝 **Author**
- 👤 0xRubusData 
- 📧 Contact: 0xRubusData@gmail.com
- 🌍 GitHub: https://github.com/0xrubusdata/Armind_os/lstm

## 🌐 Connect with Us
- **Twitter (X)**: [0xRubusData](https://x.com/Data0x88850)
- **Website**: [RubusLab](https://rubus-lab.vercel.app/)

## 🎯 **Happy Coding!** 🚀