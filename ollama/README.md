# Armind_OS Ollama API

A powerful API for interacting with Ollama models, with support for tools integration including TA-Lib for technical analysis.

## Features

- Full Ollama API support (chat, generate, embed, models)
- Tool integration with TA-Lib API
- Model validation and error handling
- Streaming responses
- Comprehensive API documentation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/0xRubusData/armind_os.git
cd armind_os/ollama
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5100 --reload
```

## Docker Support

Build and run using Docker:

```bash
docker build -t armind-ollama-api .
docker run -p 5100:5100 armind-ollama-api
```

Or using Docker Compose:

```bash
docker-compose up --build
```

## API Endpoints

### Chat

```
POST /api/v1/chat
```

Chat with a model, with optional tool support.

Example request:
```json
{
  "model": "llama2",
  "messages": [
    {"role": "user", "content": "Calculate RSI for these prices: [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42]"}
  ],
  "tools": [
    {
      "type": "function",
      "name": "talib",
      "description": "Technical Analysis Library for financial market data",
      "parameters": {
        "type": "object",
        "properties": {
          "function": {"type": "string"},
          "real": {"type": "array", "items": {"type": "number"}},
          "timeperiod": {"type": "integer", "default": 14}
        },
        "required": ["function", "real"]
      }
    }
  ]
}
```

### Generate

```
POST /api/v1/generate
```

Generate text from a prompt, with optional tool support.

Example request:
```json
{
  "model": "llama2",
  "prompt": "Calculate RSI for these prices: [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42]",
  "tools": [
    {
      "type": "function",
      "name": "talib",
      "description": "Technical Analysis Library for financial market data",
      "parameters": {
        "type": "object",
        "properties": {
          "function": {"type": "string"},
          "real": {"type": "array", "items": {"type": "number"}},
          "timeperiod": {"type": "integer", "default": 14}
        },
        "required": ["function", "real"]
      }
    }
  ]
}
```

### Embed

```
POST /api/v1/embed
```

Get embeddings for text.

Example request:
```json
{
  "model": "llama2",
  "prompt": "Hello world"
}
```

### Models

```
GET /api/v1/models
```

List all available models.

```
GET /api/v1/models/{model_name}
```

Show details of a specific model.

### Tools

```
GET /api/v1/tools
```

List all available tools.

```
GET /api/v1/tools/{tool_name}
```

Get details of a specific tool.

```
POST /api/v1/tools/{tool_name}/{endpoint}
```

Execute a tool.

Example request for TA-Lib RSI calculation:
```json
{
  "function": "RSI",
  "real": [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42],
  "timeperiod": 14
}
```

## Tool Integration

The API supports integrating with external tools, currently including:

### TA-Lib

Technical Analysis Library for financial market data. Available endpoints:

- `/api/v1/tools/talib/momentum/{function_name}` - Momentum indicators (RSI, MACD, etc.)
- `/api/v1/tools/talib/volume/{function_name}` - Volume indicators (OBV, etc.)
- `/api/v1/tools/talib/volatility/{function_name}` - Volatility indicators (ATR, etc.)
- `/api/v1/tools/talib/price/{function_name}` - Price transform functions
- `/api/v1/tools/talib/cycle/{function_name}` - Cycle indicators
- `/api/v1/tools/talib/pattern/{function_name}` - Pattern recognition
- `/api/v1/tools/talib/statistic/{function_name}` - Statistical functions
- `/api/v1/tools/talib/math/transform/{function_name}` - Math transform functions
- `/api/v1/tools/talib/math/operator/{function_name}` - Math operator functions

## Documentation

Interactive API documentation available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Error Handling

Standard HTTP status codes:
- 200: Successful request
- 400: Invalid request
- 404: Resource not found
- 422: Validation error
- 500: Server error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

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
- 🌍 GitHub: https://github.com/0xrubusdata/Armind_os/ollama

## 🌐 Connect with Us
- **Twitter (X)**: [0xRubusData](https://x.com/Data0x88850)
- **Website**: [RubusLab](https://rubus-lab.vercel.app/)

## 🎯 **Happy Coding!** 🚀