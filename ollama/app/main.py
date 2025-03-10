from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from typing import Dict, Any

from app.core.config import settings
from app.api.v1.endpoints import chat, embed, generate, show, tools

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ollama-api")

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="""
        Ollama API with tool integration.
        
        This API allows you to:
        - Generate text using Ollama models
        - Chat with Ollama models
        - Get embeddings from Ollama models
        - Manage Ollama models (list, show)
        - Use tools with Ollama models, including the TA-Lib API for technical analysis
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
    
    # Add middleware for request timing
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            process_time = time.time() - start_time
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": f"Internal server error: {str(e)}"},
                headers={"X-Process-Time": str(process_time)}
            )

    # Include routers
    app.include_router(chat.router, prefix=settings.API_V1_STR)
    app.include_router(embed.router, prefix=settings.API_V1_STR)
    app.include_router(generate.router, prefix=settings.API_V1_STR)
    app.include_router(show.router, prefix=settings.API_V1_STR)
    app.include_router(tools.router, prefix=settings.API_V1_STR)

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "name": settings.PROJECT_NAME,
            "version": "1.0.0",
            "description": "Ollama API with tool integration",
            "documentation": "/docs",
            "endpoints": {
                "chat": f"{settings.API_V1_STR}/chat",
                "generate": f"{settings.API_V1_STR}/generate",
                "embed": f"{settings.API_V1_STR}/embed",
                "models": f"{settings.API_V1_STR}/models",
                "tools": f"{settings.API_V1_STR}/tools"
            }
        }
        
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "ok"}

    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", settings.OLLAMA_PORT))
    logger.info(f"Starting FastAPI application on port {port}...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=settings.DEBUG)