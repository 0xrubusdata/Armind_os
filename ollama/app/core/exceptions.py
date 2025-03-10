from fastapi import HTTPException
from typing import Dict, Any, Optional

class OllamaError(Exception):
    """Base exception for Ollama API errors."""
    pass

class ModelNotFoundError(OllamaError):
    """Exception raised when a model is not found."""
    pass

class ToolError(Exception):
    """Base exception for tool API errors."""
    pass

class ToolNotFoundError(ToolError):
    """Exception raised when a tool or endpoint is not found."""
    pass

class ToolTimeoutError(ToolError):
    """Exception raised when a tool request times out."""
    pass

class AppException(HTTPException):
    """Base exception for application errors."""
    
    def __init__(
        self, 
        status_code: int, 
        detail: str,
        headers: Optional[Dict[str, str]] = None,
        error_code: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code or "INTERNAL_ERROR"
        self.extra = extra or {}
        super().__init__(status_code=status_code, detail=detail, headers=headers)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary."""
        return {
            "detail": self.detail,
            "error_code": self.error_code,
            "extra": self.extra
        } 