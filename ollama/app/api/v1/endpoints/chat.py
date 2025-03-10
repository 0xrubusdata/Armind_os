from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
import httpx
import json
import logging
from typing import Dict, Any, List, Optional

from app.models.request import ChatRequest
from app.services.chat_service import ChatService
from app.api.deps import get_chat_service, validate_model, validate_tools
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("")
async def chat_endpoint(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Process a chat request.
    
    Args:
        request: The chat request containing messages, model, and optional tools
        chat_service: Injected chat service
        
    Returns:
        The chat response
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
                chat_service.process_chat_stream(request),
                media_type="application/json"
            )
        else:
            return await chat_service.process_chat(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )

@router.post("/execute_tool")
async def execute_tool_endpoint(
    tool_name: str,
    endpoint: str,
    params: Dict[str, Any]
):
    """
    Execute a tool based on the model's output.
    
    Args:
        tool_name: The name of the tool to execute
        endpoint: The endpoint to call
        params: The parameters to pass to the endpoint
        
    Returns:
        The tool execution result
    """
    try:
        if tool_name == "talib":
            # Construct the full endpoint URL
            if endpoint.startswith("/"):
                endpoint = endpoint[1:]
            full_url = f"{settings.TALIB_API_URL}/{endpoint}"
            
            # Call the TA-Lib API
            async with httpx.AsyncClient() as client:
                response = await client.post(full_url, json=params)
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Error from TA-Lib API: {response.text}"
                    )
                return response.json()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool '{tool_name}' not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing tool: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing tool: {str(e)}"
        ) 