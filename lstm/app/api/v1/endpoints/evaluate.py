from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any

from app.models.request.model_request import PredictionRequest, PredictionResponse
from app.services.eval_service import EvaluationService
from app.core.exceptions import EvaluationError, ModelNotFoundError

router = APIRouter(prefix="/evaluate", tags=["evaluation"])

def get_evaluation_service() -> EvaluationService:
    return EvaluationService()

@router.post("/{model_name}/predict", response_model=PredictionResponse)
async def predict(
    model_name: str,
    request: PredictionRequest,
    service: EvaluationService = Depends(get_evaluation_service)
) -> Dict[str, Any]:
    """Make predictions using the model."""
    try:
        return service.predict(model_name, request)
    except ModelNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except EvaluationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{model_name}/evaluate")
async def evaluate_model(
    model_name: str,
    request: PredictionRequest,
    service: EvaluationService = Depends(get_evaluation_service)
) -> Dict[str, Any]:
    """Evaluate model performance on test data."""
    try:
        return service.evaluate(model_name, request)
    except ModelNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except EvaluationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 