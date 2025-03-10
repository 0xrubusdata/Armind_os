# Armind_OS TA-Lib API

A powerful and efficient REST API for technical analysis using TA-Lib, built with FastAPI.

## Features

- 150+ technical indicators organized into 10 categories
- RESTful API design with intuitive URL structure
- Comprehensive input validation and error handling
- Detailed API documentation with examples
- Rate limiting for fair usage
- Prometheus metrics for monitoring
- JSON logging for better observability
- Extensive test coverage

## Categories

1. Momentum Indicators (`/api/v1/momentum/{function_name}`)
2. Volume Indicators (`/api/v1/volume/{function_name}`)
3. Volatility Indicators (`/api/v1/volatility/{function_name}`)
4. Price Transform (`/api/v1/price/{function_name}`)
5. Cycle Indicators (`/api/v1/cycle/{function_name}`)
6. Pattern Recognition (`/api/v1/pattern/{function_name}`)
7. Statistic Functions (`/api/v1/statistic/{function_name}`)
8. Math Transform (`/api/v1/math/transform/{function_name}`)
9. Math Operators (`/api/v1/math/operator/{function_name}`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/0xRubusData/armind_os.git
cd armind_os/tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5300 --reload
```

## Docker Support

Build and run using Docker:

```bash
docker build -t armind-talib-api .
docker run -p 5300:5300 armind-talib-api
```

Or using Docker Compose:

```bash
docker-compose up --build
```

## Testing

The API includes comprehensive testing:

### Unit Tests

Run unit tests with coverage:

```bash
pytest tests/ -v --cov=app
```

Tests include:
- Request validation
- Model validation
- Error handling
- Rate limiting
- API endpoints

### Integration Tests

Integration tests cover:
- End-to-end API functionality
- Data consistency
- Error scenarios
- Rate limiting behavior
- Middleware functionality

### Load Testing

Run load tests using Locust:

```bash
locust -f tests/locustfile.py --host=http://localhost:5300
```

Then open http://localhost:8089 to start the load test.

Load tests simulate:
- Multiple concurrent users
- Various API endpoints
- Different request patterns
- Error scenarios
- Performance under load

## Monitoring

### Prometheus Metrics

The API exposes Prometheus metrics at `/metrics`, including:

- Request latencies
- Request counts by endpoint
- Error counts by type
- Active requests
- Memory and CPU usage
- Custom TA-Lib function metrics

Example Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'talib-api'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:5300']
```

### Logging

Enhanced JSON logging includes:

- Request details
- Processing time
- Error information
- Function call details
- System metrics

Log format:
```json
{
  "timestamp": "2024-03-10T12:34:56.789Z",
  "level": "INFO",
  "module": "main",
  "function": "calculate_indicator",
  "message": "Request processed",
  "client_ip": "127.0.0.1",
  "method": "POST",
  "path": "/api/v1/momentum/RSI",
  "processing_time": "0.0123s"
}
```

## Rate Limiting

The API implements rate limiting:

- Per-minute limit: 100 requests
- Per-hour limit: 1000 requests

Rate limit information in response headers:
- X-RateLimit-Limit-Minute
- X-RateLimit-Remaining-Minute
- X-RateLimit-Limit-Hour
- X-RateLimit-Remaining-Hour

## API Documentation

Interactive API documentation available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Error Handling

Standard HTTP status codes:
- 200: Successful calculation
- 400: Invalid parameters
- 404: Function not found
- 422: Validation error
- 429: Rate limit exceeded
- 500: Calculation error

Error response format:
```json
{
  "error_code": "ERROR_TYPE",
  "detail": "Error description",
  "extra": {
    "additional": "information"
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- [TA-Lib](https://ta-lib.org/) - Technical Analysis Library
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework

## 📜 License
MIT License - Free to use and contribute!

## 📝 **Author**
- 👤 0xRubusData 
- 📧 Contact: 0xRubusData@gmail.com
- 🌍 GitHub: https://github.com/0xRubusData/armind_os/tool

## 🌐 Connect with Us
- **Twitter (X)**: [0xRubusData](https://x.com/Data0x88850)
- **Website**: [RubusLab](https://rubus-lab.vercel.app/)

## 🤝 Contributing
Contributions are welcome! Open an issue or submit a PR.

---
🚀 **Stay tuned for updates as Rubus-Code evolves!**