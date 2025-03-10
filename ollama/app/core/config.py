from pydantic_settings import BaseSettings
from typing import Optional, List, Dict, Any
import os
import httpx
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # API Settings
    OLLAMA_PORT: int = 5100
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Ollama API"
    
    # Ollama API URL
    OLLAMA_API_URL: str = "http://localhost:11434"
    
    # Default model settings
    DEFAULT_MODEL: str = "llama2"
    AVAILABLE_MODELS: List[str] = []
    
    # Tool settings
    TALIB_API_URL: str = "http://localhost:5300/api/v1"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True
        
    def get_available_models(self) -> List[str]:
        """Fetch available models from Ollama API."""
        if self.AVAILABLE_MODELS:
            return self.AVAILABLE_MODELS
            
        try:
            response = httpx.get(f"{self.OLLAMA_API_URL}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                self.AVAILABLE_MODELS = [model["name"] for model in models_data.get("models", [])]
                return self.AVAILABLE_MODELS
            else:
                logger.warning(f"Failed to fetch models: {response.status_code}")
                return [self.DEFAULT_MODEL]
        except Exception as e:
            logger.error(f"Error fetching models: {str(e)}")
            return [self.DEFAULT_MODEL]

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

settings = get_settings() 