from typing import Dict, Any
import logging

from app.models.request import EmbedRequest
from app.core.logging import logger
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)

class EmbedService(BaseService):
    """Service for handling text embedding operations."""

    async def process_embed(self, request: EmbedRequest) -> Dict[str, Any]:
        """
        Process an embed request to get text embeddings.

        Args:
            request: The embed request containing prompt and model

        Returns:
            The processed embedding response

        Raises:
            OllamaError: If there's an error with the Ollama service
            ModelNotFoundError: If the specified model is not found
        """
        try:
            await self.log_request(
                "embed",
                model=request.model,
                prompt=request.prompt
            )
            
            # Prepare the request data
            data = {
                "model": request.model,
                "prompt": request.prompt
            }
            
            # Add optional parameters if provided
            if request.options:
                data["options"] = request.options
                
            # Call the Ollama API
            response = await self.call_ollama_api("embeddings", data)
            return await self.handle_ollama_response(response)

        except Exception as e:
            logger.error(f"Error in embed service: {str(e)}")
            raise
