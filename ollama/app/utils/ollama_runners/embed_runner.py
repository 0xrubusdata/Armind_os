from typing import Dict, Any, Optional, Union, List
import httpx
from app.core.logging import logger
from app.models.request.options_request import OptionsRequest

async def sync_ollama_embed(
    model: str,
    input_text: Union[str, List[str]],
    options: Optional[OptionsRequest] = None
) -> Dict[str, Any]:
    """
    Get embeddings from Ollama.
    
    Args:
        model: The model to use for embeddings
        input_text: The text to embed (string or list of strings)
        options: Optional embedding options
        
    Returns:
        The Ollama response containing embeddings
    """
    url = f"http://localhost:11434/api/embeddings"
    
    payload = {
        "model": model,
        "prompt": input_text
    }
    
    if options:
        payload["options"] = options.dict(exclude_none=True)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error in embed: {str(e)}")
        raise 