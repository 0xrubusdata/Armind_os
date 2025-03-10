from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any

from app.models.request.model_request import TrainingRequest, TrainingResponse
from app.services.train_service import TrainingService
from app.core.exceptions import TrainingError, ModelNotFoundError

router = APIRouter(prefix="/train", tags=["training"])

def get_training_service() -> TrainingService:
    return TrainingService()

@router.post("/{model_name}", response_model=TrainingResponse)
async def train_model(
    model_name: str,
    request: TrainingRequest,
    service: TrainingService = Depends(get_training_service)
) -> Dict[str, Any]:
    """Train a model with provided data."""
    try:
        return service.train_model(model_name, request)
    except ModelNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TrainingError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 