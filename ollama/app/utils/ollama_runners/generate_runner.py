from typing import Dict, Any, Optional
import httpx
from app.core.config import settings
from app.core.logging import logger

async def sync_ollama_generate(
    model: str,
    prompt: str,
    system: Optional[str] = None,
    stream: bool = False
) -> Dict[str, Any]:
    """
    Synchronously generate text using Ollama.
    
    Args:
        model: The model to use for generation
        prompt: The prompt for text generation
        system: Optional system message
        stream: Whether to stream the response
        
    Returns:
        The Ollama response
    """
    url = f"http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    if system:
        payload["system"] = system
        
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error in sync generate: {str(e)}")
        raise

async def async_ollama_generate(
    model: str,
    prompt: str,
    system: Optional[str] = None,
    stream: bool = False
) -> Dict[str, Any]:
    """
    Asynchronously generate text using Ollama.
    
    Args:
        model: The model to use for generation
        prompt: The prompt for text generation
        system: Optional system message
        stream: Whether to stream the response
        
    Returns:
        The Ollama response
    """
    url = f"http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    if system:
        payload["system"] = system
        
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error in async generate: {str(e)}")
        raise 