from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import time
import asyncio
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.exceptions import AppException, TalibException
from app.api.v1.endpoints.talib import router as talib_router
from app.core.logging import logger, log_request_details, log_function_call
from app.core.middleware.rate_limit import RateLimitMiddleware
from app.core.metrics import instrument_app, ACTIVE_REQUESTS, ERROR_COUNTER
from app.core.cache import periodic_cleanup

# Store start time for uptime calculation
start_time = time.time()

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="""
        # TA-Lib API Documentation

        This API provides access to the TA-Lib technical analysis library through a RESTful interface.
        It allows you to calculate various technical indicators for financial market data.

        ## Key Features
        - **150+ Technical Indicators**: Access to all TA-Lib functions
        - **Real-time Calculations**: Fast and efficient processing
        - **Input Validation**: Comprehensive validation of all inputs
        - **Rate Limiting**: Fair usage limits
        - **Prometheus Metrics**: Built-in monitoring
        - **JSON Logging**: Detailed request tracking
        - **Result Caching**: Improved performance for repeated calculations

        ## Quick Start Guide

        ### 1. Simple Moving Average (SMA) Example
        ```json
        POST /api/v1/talib/overlap/SMA
        {
            "real": [10.0, 11.0, 12.0, 13.0, 14.0],
            "timeperiod": 3
        }
        ```
        Response:
        ```json
        {
            "function": "SMA",
            "category": "Overlap Studies",
            "results": {
                "real": [null, null, 11.0, 12.0, 13.0]
            }
        }
        ```

        ### 2. Relative Strength Index (RSI) Example
        ```json
        POST /api/v1/talib/momentum/RSI
        {
            "real": [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42],
            "timeperiod": 14
        }
        ```
        Response:
        ```json
        {
            "function": "RSI",
            "category": "Momentum Indicators",
            "results": {
                "real": [null, null, null, null, 51.78, 54.65, 55.27, 56.44]
            }
        }
        ```

        ### 3. Bollinger Bands Example
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
        Response:
        ```json
        {
            "function": "BBANDS",
            "category": "Overlap Studies",
            "results": {
                "upperband": [null, null, null, null, 45.81, 46.06, 46.42, 46.89],
                "middleband": [null, null, null, null, 44.10, 44.40, 44.59, 44.85],
                "lowerband": [null, null, null, null, 42.39, 42.74, 42.76, 42.81]
            }
        }
        ```

        ## Common Use Cases

        1. **Trend Analysis**
           - Moving Averages (SMA, EMA, WMA)
           - MACD
           - ADX
           - Parabolic SAR

        2. **Momentum Analysis**
           - RSI
           - Stochastic
           - CCI
           - ROC

        3. **Volatility Analysis**
           - Bollinger Bands
           - ATR
           - Standard Deviation

        4. **Volume Analysis**
           - OBV
           - Money Flow Index
           - Volume Rate of Change

        ## Rate Limits
        - {settings.RATE_LIMIT_PER_MINUTE} requests per minute
        - {settings.RATE_LIMIT_PER_HOUR} requests per hour

        ## Response Headers
        - `X-RateLimit-Limit-Minute`: Maximum requests per minute
        - `X-RateLimit-Remaining-Minute`: Remaining requests this minute
        - `X-RateLimit-Limit-Hour`: Maximum requests per hour
        - `X-RateLimit-Remaining-Hour`: Remaining requests this hour
        - `X-Process-Time`: Processing time in seconds
        - `X-Cache`: HIT/MISS - Indicates if result was from cache

        ## Error Codes
        - 400: Bad Request - Invalid parameters
        - 404: Not Found - Function not found
        - 422: Validation Error - Invalid input data
        - 429: Too Many Requests - Rate limit exceeded
        - 500: Internal Server Error - Calculation error

        ## Error Response Examples

        ### Invalid Parameters
        ```json
        {
            "error_code": "INVALID_PARAMETERS",
            "detail": "Invalid timeperiod parameter",
            "status_code": 400,
            "extra": {
                "parameter": "timeperiod",
                "reason": "Must be greater than 0"
            }
        }
        ```

        ### Rate Limit Exceeded
        ```json
        {
            "error_code": "RATE_LIMIT_EXCEEDED",
            "detail": "Rate limit exceeded",
            "status_code": 429,
            "extra": {
                "retry_after": "60 seconds"
            }
        }
        ```

        ## Additional Resources
        - [TA-Lib Documentation](https://ta-lib.org/function.html)
        - [Postman Collection](/docs/postman_collection.json)
        - [OpenAPI Specification](/api/v1/openapi.json)
        - [Metrics Dashboard](/metrics)
        """,
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    
    # Add rate limiting middleware
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=settings.RATE_LIMIT_PER_MINUTE,
        requests_per_hour=settings.RATE_LIMIT_PER_HOUR
    )
    
    # Set up Prometheus metrics
    metrics_instrumentator = instrument_app()
    metrics_instrumentator.instrument(app)
    
    # Start cache cleanup task
    @app.on_event("startup")
    async def start_cache_cleanup():
        asyncio.create_task(periodic_cleanup())
    
    # Add middleware for request timing and logging
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        
        # Increment active requests
        ACTIVE_REQUESTS.inc()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log request details
            log_request_details(request, process_time)
            
            # Add processing time header
            response.headers["X-Process-Time"] = str(process_time)
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            
            # Log error
            log_request_details(request, process_time, error=e)
            ERROR_COUNTER.labels(error_type=type(e).__name__).inc()
            
            raise
            
        finally:
            # Decrement active requests
            ACTIVE_REQUESTS.dec()
    
    # Exception handlers
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        ERROR_COUNTER.labels(error_type="AppException").inc()
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(),
        )
    
    @app.exception_handler(TalibException)
    async def talib_exception_handler(request: Request, exc: TalibException):
        ERROR_COUNTER.labels(error_type="TalibException").inc()
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(),
        )
        
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        ERROR_COUNTER.labels(error_type="ValidationError").inc()
        errors = []
        for error in exc.errors():
            errors.append({
                "loc": error.get("loc", []),
                "msg": error.get("msg", ""),
                "type": error.get("type", "")
            })
        return JSONResponse(
            status_code=422,
            content={
                "error_code": "VALIDATION_ERROR",
                "detail": "Request validation error",
                "errors": errors,
                "status_code": 422
            },
        )

    # Include routers
    app.include_router(talib_router, prefix=settings.API_V1_STR)

    # Mount static files
    app.mount("/docs/static", StaticFiles(directory="docs"), name="docs")

    @app.get("/", tags=["General"])
    async def root():
        """Root endpoint that provides API information."""
        return {
            "name": settings.PROJECT_NAME,
            "version": "1.0.0",
            "description": "Technical Analysis Library API",
            "documentation": "/docs",
            "health_check": "/health",
            "metrics": "/metrics",
            "api_prefix": settings.API_V1_STR
        }
    
    @app.get("/health", tags=["Monitoring"])
    async def health_check():
        """
        Health check endpoint that provides detailed system status.
        
        Returns:
            dict: Health status information including:
                - status: Current health status
                - version: API version
                - timestamp: Current timestamp
                - uptime: Server uptime
                - active_requests: Number of active requests
                - rate_limits: Current rate limit settings
        """
        return {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": time.time(),
            "uptime": time.time() - start_time,
            "active_requests": ACTIVE_REQUESTS._value.get(),
            "rate_limits": {
                "per_minute": settings.RATE_LIMIT_PER_MINUTE,
                "per_hour": settings.RATE_LIMIT_PER_HOUR
            }
        }

    return app

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Custom extension to add category-specific documentation
    openapi_schema["tags"] = [
        {
            "name": "General",
            "description": "General API information and root endpoints",
        },
        {
            "name": "Monitoring",
            "description": "Health check and metrics endpoints",
        },
        {
            "name": "talib",
            "description": "Technical Analysis Library functions",
            "externalDocs": {
                "description": "TA-Lib Documentation",
                "url": "https://ta-lib.org/function.html",
            },
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = create_application()

# Custom OpenAPI schema
app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=settings.TOOL_PORT, 
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )