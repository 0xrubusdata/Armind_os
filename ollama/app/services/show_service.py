from typing import Dict, Any
import logging

from app.core.logging import logger
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)

class ShowService(BaseService):
    """Service for handling model information retrieval operations."""

    async def show_model(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific model.

        Args:
            model_name: The name of the model to show

        Returns:
            The model information

        Raises:
            OllamaError: If there's an error with the Ollama service
            ModelNotFoundError: If the specified model is not found
        """
        try:
            await self.log_request("show", model=model_name)
            
            # Call the Ollama API
            response = await self.call_ollama_api("show", {"name": model_name})
            return await self.handle_ollama_response(response)

        except Exception as e:
            logger.error(f"Error in show service: {str(e)}")
            raise