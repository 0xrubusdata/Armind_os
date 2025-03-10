from fastapi import HTTPException
from typing import Any, Dict, Optional

class AppException(HTTPException):
    """
    Base exception class for application-specific exceptions.
    
    This class extends FastAPI's HTTPException to provide a standardized way
    to raise and handle exceptions throughout the application.
    
    Attributes:
        status_code: HTTP status code
        detail: Error message
        headers: Optional HTTP headers
        error_code: Application-specific error code
        extra: Additional error information
    """
    def __init__(
        self, 
        status_code: int, 
        detail: str,
        headers: Optional[Dict[str, str]] = None,
        error_code: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code or f"APP_{status_code}"
        self.extra = extra or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary for JSON response."""
        return {
            "error_code": self.error_code,
            "detail": self.detail,
            "status_code": self.status_code,
            **self.extra
        }


class TalibException(AppException):
    """Base exception class for TA-Lib related errors."""
    def __init__(
        self, 
        status_code: int, 
        detail: str,
        error_code: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        error_code = error_code or f"TALIB_{status_code}"
        super().__init__(status_code=status_code, detail=detail, error_code=error_code, extra=extra)


class FunctionNotFoundException(TalibException):
    """Exception raised when a TA-Lib function is not found."""
    def __init__(self, function_name: str, category: Optional[str] = None):
        detail = f"Function '{function_name}' not found"
        if category:
            detail += f" in category '{category}'"
        super().__init__(
            status_code=404,
            detail=detail,
            error_code="TALIB_FUNCTION_NOT_FOUND",
            extra={"function_name": function_name, "category": category}
        )


class CategoryNotFoundException(TalibException):
    """Exception raised when a TA-Lib category is not found."""
    def __init__(self, category: str):
        super().__init__(
            status_code=404,
            detail=f"Category '{category}' not found",
            error_code="TALIB_CATEGORY_NOT_FOUND",
            extra={"category": category}
        )


class InvalidParameterException(TalibException):
    """Exception raised when invalid parameters are provided to a TA-Lib function."""
    def __init__(self, function_name: str, missing_params: Optional[list] = None, invalid_params: Optional[Dict[str, str]] = None):
        detail = f"Invalid parameters for function '{function_name}'"
        extra = {"function_name": function_name}
        
        if missing_params:
            detail += f". Missing required parameters: {', '.join(missing_params)}"
            extra["missing_params"] = missing_params
            
        if invalid_params:
            detail += f". Invalid parameters: {invalid_params}"
            extra["invalid_params"] = invalid_params
            
        super().__init__(
            status_code=400,
            detail=detail,
            error_code="TALIB_INVALID_PARAMETERS",
            extra=extra
        )


class CalculationException(TalibException):
    """Exception raised when a TA-Lib calculation fails."""
    def __init__(self, function_name: str, error_message: str):
        super().__init__(
            status_code=500,
            detail=f"Error calculating '{function_name}': {error_message}",
            error_code="TALIB_CALCULATION_ERROR",
            extra={"function_name": function_name, "error_message": error_message}
        )


# Legacy exceptions - kept for backward compatibility
class TollBaseException(AppException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail, error_code=f"TOLL_{status_code}")

class TollError(TollBaseException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Toll error: {detail}")

class ModelNotFoundError(TollBaseException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Toll model not found or unreachable"
        )

class ValidationError(TollBaseException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=422,
            detail=f"Validation error: {detail}"
        ) 