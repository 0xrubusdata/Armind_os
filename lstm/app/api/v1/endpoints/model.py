from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Any

from app.models.request.model_request import ModelRequest, ModelResponse
from app.services.model_service import ModelService
from app.core.exceptions import LSTMError

router = APIRouter(prefix="/model", tags=["model"])

def get_model_service() -> ModelService:
    return ModelService()

@router.post("/", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def create_model(
    request: ModelRequest,
    service: ModelService = Depends(get_model_service)
) -> Dict[str, Any]:
    """Create a new LSTM model."""
    try:
        return service.create_model(request)
    except LSTMError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{model_name}", response_model=ModelResponse)
async def get_model(
    model_name: str,
    service: ModelService = Depends(get_model_service)
) -> Dict[str, Any]:
    """Get model information."""
    try:
        return service.get_model_info(model_name)
    except LSTMError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/", response_model=List[ModelResponse])
async def list_models(
    service: ModelService = Depends(get_model_service)
) -> List[Dict[str, Any]]:
    """List all available models."""
    try:
        return service.list_models()
    except LSTMError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{model_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(
    model_name: str,
    service: ModelService = Depends(get_model_service)
):
    """Delete a model."""
    try:
        service.delete_model(model_name)
    except LSTMError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 