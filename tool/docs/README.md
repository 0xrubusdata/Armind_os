# TA-Lib API Documentation

This directory contains additional documentation and resources for the TA-Lib API.

## Contents

1. **Postman Collection**
   - File: `postman_collection.json`
   - Import this file into Postman to get started quickly
   - Contains example requests for all major endpoints
   - Includes environment variables for easy configuration

## Using the Postman Collection

1. Download [Postman](https://www.postman.com/downloads/)
2. Import the collection:
   - Click "Import" in Postman
   - Select the `postman_collection.json` file
   - The collection will appear in your workspace

3. Configure the environment:
   - Create a new environment in Postman
   - Add a variable named `base_url`
   - Set its value to your API base URL (e.g., `http://localhost:5300`)

4. Start making requests:
   - Expand the collection to see available requests
   - Each request includes example data
   - Modify the request body as needed

## Example Requests

### 1. Simple Moving Average (SMA)
```json
POST /api/v1/talib/overlap/SMA
{
    "real": [10.0, 11.0, 12.0, 13.0, 14.0],
    "timeperiod": 3
}
```

### 2. Relative Strength Index (RSI)
```json
POST /api/v1/talib/momentum/RSI
{
    "real": [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42],
    "timeperiod": 14
}
```

### 3. Bollinger Bands (BBANDS)
```json
POST /api/v1/talib/overlap/BBANDS
{
    "real": [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42],
    "timeperiod": 5,
    "nbdevup": 2,
    "nbdevdn": 2,
    "matype": 0
}
```

### 4. Moving Average Convergence/Divergence (MACD)
```json
POST /api/v1/talib/momentum/MACD
{
    "real": [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42],
    "fastperiod": 12,
    "slowperiod": 26,
    "signalperiod": 9
}
```

### 5. Average True Range (ATR)
```json
POST /api/v1/talib/volatility/ATR
{
    "high": [44.34, 44.09, 44.15, 43.61, 44.33],
    "low": [44.20, 44.00, 44.03, 43.50, 44.15],
    "close": [44.23, 44.05, 44.10, 43.55, 44.23],
    "timeperiod": 14
}
```

## Common Parameters

Many indicators share common parameters:

- `timeperiod`: Number of periods to calculate over
- `real`: Array of price values for single-input functions
- `high`, `low`, `close`: Arrays of price data for multi-input functions
- `volume`: Array of volume data for volume-based indicators

## Response Format

All responses follow this general format:
```json
{
    "function": "FUNCTION_NAME",
    "category": "CATEGORY_NAME",
    "results": {
        "output_name": [values...]
    }
}
```

## Error Handling

The API uses standard HTTP status codes and returns detailed error messages:

```json
{
    "error_code": "ERROR_TYPE",
    "detail": "Error description",
    "status_code": 400,
    "extra": {
        "additional": "error info"
    }
}
```

## Rate Limiting

The API implements rate limiting:
- Headers indicate your current limits and usage
- Exceeded limits return 429 status code
- Includes retry-after information

## Additional Resources

- [API Documentation](/docs)
- [OpenAPI Specification](/api/v1/openapi.json)
- [TA-Lib Official Documentation](https://ta-lib.org/function.html) 