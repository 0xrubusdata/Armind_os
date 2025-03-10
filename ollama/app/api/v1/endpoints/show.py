from fastapi import APIRouter, Depends, HTTPException, status, Path
import logging
from typing import Dict, Any, List, Optional

from app.services.show_service import ShowService
from app.api.deps import get_show_service, validate_model
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/models", tags=["models"])

@router.get("")
async def list_models_endpoint():
    """
    List all available models.
    
    Returns:
        List of available models
    """
    try:
        models = settings.get_available_models()
        return {"models": models}
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing models: {str(e)}"
        )

@router.get("/{model_name}")
async def show_model_endpoint(
    model_name: str = Path(..., description="The name of the model to show"),
    show_service: ShowService = Depends(get_show_service)
):
    """
    Show details of a specific model.
    
    Args:
        model_name: The name of the model to show
        show_service: Injected show service
        
    Returns:
        The model details
    """
    try:
        # Validate model
        validated_model = await validate_model(model_name)
        
        # Process request
        return await show_service.show_model(validated_model)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error showing model {model_name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error showing model: {str(e)}"
        ) 