from fastapi import APIRouter, HTTPException
from app.services.generate_service import get_generate_response
from app.models.request.request_models import ChatRequest, EmbedRequest
from app.models.request.generate_request import GenerateRequest
from app.models.dto.generate_dto import GenerateDto

router = APIRouter()

@router.post("/api/generate")
def generate_endpoint(generate_request: GenerateRequest, sync: bool=True):
    try:
        # Transform GenerateRequest into GenerateDto
        generate_dto = GenerateDto.build(generate_request, sync, False)
        
        return get_generate_response(generate_dto)
    except HTTPException as e:
        # The exception is propagated with the correct code (404 or other)
        raise e
    except Exception as e:
        # For any other type of error, return a 500 status
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/api/generate_stream")
def generate_endpoint(generate_request: GenerateRequest, sync: bool=True):
    try:
        # Transform GenerateRequest into GenerateDto
        generate_dto = GenerateDto.build(generate_request, sync, True)
        
        return get_generate_response(generate_dto)
    except HTTPException as e:
        # The exception is propagated with the correct code (404 or other)
        raise e
    except Exception as e:
        # For any other type of error, return a 500 status
        raise HTTPException(status_code=500, detail=str(e))    