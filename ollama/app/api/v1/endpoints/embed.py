from fastapi import APIRouter, Depends, HTTPException, status
import logging
from typing import Dict, Any, List, Optional

from app.models.request import EmbedRequest
from app.services.embed_service import EmbedService
from app.api.deps import get_embed_service, validate_model
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/embed", tags=["embed"])

@router.post("")
async def embed_endpoint(
    request: EmbedRequest,
    embed_service: EmbedService = Depends(get_embed_service)
):
    """
    Generate embeddings for text.
    
    Args:
        request: The embed request containing prompt and model
        embed_service: Injected embed service
        
    Returns:
        The embeddings response
    """
    try:
        # Validate model
        validated_model = await validate_model(request.model)
        if validated_model != request.model:
            logger.info(f"Using model '{validated_model}' instead of requested '{request.model}'")
            request.model = validated_model
            
        # Process request
        return await embed_service.process_embed(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in embed endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing embed request: {str(e)}"
        ) 