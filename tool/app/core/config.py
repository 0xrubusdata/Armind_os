from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    PROJECT_NAME: str = "Armind_OS TA-Lib API"
    API_V1_STR: str = "/api/v1"
    TOOL_PORT: int = 5300
    DEBUG: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # CORS Settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cache Settings
    CACHE_TTL: int = 3600  # 1 hour in seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 