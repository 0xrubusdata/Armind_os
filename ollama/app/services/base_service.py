from typing import Dict, Any, AsyncGenerator
import logging

from app.core.logging import logger
from app.utils.ollama_client import ollama_client
from app.utils.tool_client import tool_client

logger = logging.getLogger(__name__)

class BaseService:
    """Base service class with common functionality for all services."""
    
    async def handle_ollama_response(self, response: Dict[str, Any]) -> Any:
        """
        Handle the response from Ollama API.
        
        Args:
            response: The response from Ollama API
            
        Returns:
            The processed response
        """
        return response
    
    async def call_ollama_api(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the Ollama API.
        
        Args:
            endpoint: The API endpoint to call
            data: The data to send
            
        Returns:
            The response from the Ollama API
        """
        return await ollama_client._make_request(endpoint, data)
    
    async def stream_ollama_api(self, endpoint: str, data: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream from the Ollama API.
        
        Args:
            endpoint: The API endpoint to call
            data: The data to send
            
        Yields:
            The streaming responses from the Ollama API
        """
        async for chunk in ollama_client._make_request(endpoint, data, stream=True):
            yield chunk
    
    async def execute_tool(self, tool_name: str, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool.
        
        Args:
            tool_name: The name of the tool to execute
            endpoint: The endpoint to call
            params: The parameters to pass to the endpoint
            
        Returns:
            The tool execution result
        """
        return await tool_client.execute_tool(tool_name, endpoint, params)
    
    async def log_request(self, method: str, **kwargs) -> None:
        """Log the request details."""
        logger.debug(
            f"Request to {method} with args: {kwargs}"
        )