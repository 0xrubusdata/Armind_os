from typing import Generator, List, Dict, Any, Optional
from fastapi import Depends, HTTPException, status
import httpx
import logging

from app.services.chat_service import ChatService
from app.services.embed_service import EmbedService
from app.services.generate_service import GenerateService
from app.services.show_service import ShowService
from app.services.tools_service import ToolsService
from app.core.config import settings

logger = logging.getLogger(__name__)

async def validate_model(model: str) -> str:
    """
    Validate that the requested model exists in Ollama.
    
    Args:
        model: The model name to validate
        
    Returns:
        The validated model name
        
    Raises:
        HTTPException: If the model doesn't exist
    """
    if not model:
        return settings.DEFAULT_MODEL
        
    try:
        # Check if model is in cached list
        available_models = settings.get_available_models()
        if model in available_models:
            return model
            
        # If not in cache, try to fetch fresh list
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_API_URL}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                available_models = [m["name"] for m in models_data.get("models", [])]
                settings.AVAILABLE_MODELS = available_models
                
                if model in available_models:
                    return model
                    
                # Model not found
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Model '{model}' not found. Available models: {', '.join(available_models)}"
                )
            else:
                # Couldn't fetch models, use default
                logger.warning(f"Failed to fetch models: {response.status_code}")
                if model == settings.DEFAULT_MODEL:
                    return model
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Unable to validate model. Ollama service may be unavailable."
                )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating model: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating model: {str(e)}"
        )

async def validate_tools(tools: Optional[List[Dict[str, Any]]] = None) -> Optional[List[Dict[str, Any]]]:
    """
    Validate that the requested tools exist and are properly configured.
    
    Args:
        tools: List of tools to validate
        
    Returns:
        The validated tools list
    """
    if not tools:
        return None
        
    validated_tools = []
    
    for tool in tools:
        tool_name = tool.get("name")
        if not tool_name:
            continue
            
        # Validate talib tool
        if tool_name == "talib":
            try:
                # Check if talib API is available
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{settings.TALIB_API_URL}/talib/categories")
                    if response.status_code == 200:
                        # Tool is valid, add it to the list
                        validated_tools.append(tool)
                    else:
                        logger.warning(f"TA-Lib API not available: {response.status_code}")
            except Exception as e:
                logger.error(f"Error validating TA-Lib tool: {str(e)}")
        else:
            # Unknown tool, skip it
            logger.warning(f"Unknown tool: {tool_name}")
            
    return validated_tools if validated_tools else None

def get_chat_service() -> Generator[ChatService, None, None]:
    """Dependency for chat service."""
    service = ChatService()
    try:
        yield service
    finally:
        pass

def get_embed_service() -> Generator[EmbedService, None, None]:
    """Dependency for embed service."""
    service = EmbedService()
    try:
        yield service
    finally:
        pass

def get_generate_service() -> Generator[GenerateService, None, None]:
    """Dependency for generate service."""
    service = GenerateService()
    try:
        yield service
    finally:
        pass

def get_show_service() -> Generator[ShowService, None, None]:
    """Dependency for show service."""
    service = ShowService()
    try:
        yield service
    finally:
        pass

def get_tools_service() -> Generator[ToolsService, None, None]:
    """Dependency for tools service."""
    service = ToolsService()
    try:
        yield service
    finally:
        pass 