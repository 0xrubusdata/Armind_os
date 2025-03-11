from pydantic_settings import BaseSettings
from typing import Dict, Any, Optional
import torch

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FAISS API"
    
    # Default model settings
    class Config:
        env_file = ".env"

settings = Settings() 