from fastapi import APIRouter, Depends
from typing import Callable, Dict, Any
from functools import wraps

from app.services.talib_service import TalibService
from app.api.deps import get_talib_service
from app.core.logging import logger
from app.models.dto.talib_dto_factory import TalibDtoFactory
from app.core.exceptions import (
    AppException,
    CalculationException
)

def create_category_router(category_name: str) -> APIRouter:
    """Create a router for a specific TA-Lib category."""
    return APIRouter(
        responses={
            404: {"description": "Function not found"},
            400: {"description": "Invalid parameters"},
            500: {"description": "Calculation error"}
        }
    )

def talib_endpoint(category: str, dictionary_name: str):
    """
    Decorator for TA-Lib endpoints to reduce code duplication.
    
    Args:
        category: Human-readable category name
        dictionary_name: Dictionary name for function lookup
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(function_name: str, data, talib_service: TalibService = Depends(get_talib_service)):
            try:
                logger.info(f"Processing {category} function: {function_name}")
                talib_dto = TalibDtoFactory.build(function_name, dictionary_name, data)
                result = await talib_service.process_talib_request(function_name, talib_dto, category)
                logger.info(f"Successfully processed {category} function: {function_name}")
                return result
            except AppException as e:
                logger.warning(f"Application error in {category} function {function_name}: {e.detail}")
                raise e
            except Exception as e:
                logger.error(f"Unexpected error in {category} function {function_name}: {str(e)}", exc_info=True)
                raise CalculationException(function_name, str(e))
        return wrapper
    return decorator 