from typing import Dict, Any
import httpx
from app.core.logging import logger

async def sync_ollama_show(model: str) -> Dict[str, Any]:
    """
    Get model information from Ollama.
    
    Args:
        model: The model name to get information about
        
    Returns:
        The Ollama response containing model information
    """
    url = f"http://localhost:11434/api/show"
    
    payload = {
        "name": model
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error in show: {str(e)}")
        raise 