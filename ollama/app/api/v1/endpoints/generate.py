from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
import logging
from typing import Dict, Any, List, Optional

from app.models.request import GenerateRequest
from app.services.generate_service import GenerateService
from app.api.deps import get_generate_service, validate_model, validate_tools
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/generate", tags=["generate"])

@router.post("")
async def generate_endpoint(
    request: GenerateRequest,
    generate_service: GenerateService = Depends(get_generate_service)
):
    """
    Generate text from a prompt.
    
    Args:
        request: The generate request containing prompt, model, and optional tools
        generate_service: Injected generate service
        
    Returns:
        The generated text response
    """
    try:
        # Validate model
        validated_model = await validate_model(request.model)
        if validated_model != request.model:
            logger.info(f"Using model '{validated_model}' instead of requested '{request.model}'")
            request.model = validated_model
            
        # Validate tools
        validated_tools = await validate_tools(request.tools)
        request.tools = validated_tools
        
        # Process request
        if request.stream:
            return StreamingResponse(
                generate_service.process_generate_stream(request),
                media_type="application/json"
            )
        else:
            return await generate_service.process_generate(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing generate request: {str(e)}"
        )

@router.post("/stream")
async def generate_stream_endpoint(
    generate_request: GenerateRequest,
    sync: bool = True,
    generate_service: GenerateService = Depends(get_generate_service)
):
    """
    Process a streaming generate request.
    
    Args:
        generate_request: The generate request containing prompt and system message
        sync: Whether to process synchronously
        generate_service: Injected generate service
        
    Returns:
        The streaming generation response
    """
    try:
        return await generate_service.process_generate(generate_request, sync, stream=True)
    except Exception as e:
        logger.error(f"Error in generate stream endpoint: {str(e)}")
        raise 