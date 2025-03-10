from typing import Dict, Any, Optional, Union, List, AsyncGenerator
import httpx
import json
import logging
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.config import settings
from app.core.exceptions import OllamaError, ModelNotFoundError

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with the Ollama API."""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: The base URL for the Ollama API. If not provided, uses the URL from settings.
        """
        self.base_url = base_url or settings.OLLAMA_API_URL
        self.timeout = httpx.Timeout(60.0, connect=10.0)
        self.limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True
    )
    async def _make_request(
        self, 
        endpoint: str, 
        data: Dict[str, Any],
        stream: bool = False
    ) -> Union[Dict[str, Any], AsyncGenerator[Dict[str, Any], None]]:
        """
        Make a request to the Ollama API.
        
        Args:
            endpoint: The API endpoint to call
            data: The data to send
            stream: Whether to stream the response
            
        Returns:
            The response from the Ollama API
            
        Raises:
            OllamaError: If there's an error calling the API
            ModelNotFoundError: If the specified model is not found
        """
        url = f"{self.base_url}/api/{endpoint}"
        
        try:
            if stream:
                return self._stream_request(url, data)
            else:
                async with httpx.AsyncClient(timeout=self.timeout, limits=self.limits) as client:
                    response = await client.post(url, json=data)
                    response.raise_for_status()
                    return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error calling Ollama API: {str(e)}")
            if e.response.status_code == 404 and "model not found" in e.response.text.lower():
                raise ModelNotFoundError()
            raise OllamaError(f"HTTP error: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error calling Ollama API: {str(e)}")
            raise OllamaError(f"Request error: {str(e)}")
        except Exception as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            raise OllamaError(f"Error: {str(e)}")
            
    async def _stream_request(self, url: str, data: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream a request to the Ollama API.
        
        Args:
            url: The URL to call
            data: The data to send
            
        Yields:
            The streaming responses from the Ollama API
            
        Raises:
            OllamaError: If there's an error streaming from the API
            ModelNotFoundError: If the specified model is not found
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout, limits=self.limits) as client:
                async with client.stream("POST", url, json=data) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to decode JSON: {line}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error streaming from Ollama API: {str(e)}")
            if e.response.status_code == 404 and "model not found" in e.response.text.lower():
                raise ModelNotFoundError()
            raise OllamaError(f"HTTP error: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error streaming from Ollama API: {str(e)}")
            raise OllamaError(f"Request error: {str(e)}")
        except Exception as e:
            logger.error(f"Error streaming from Ollama API: {str(e)}")
            raise OllamaError(f"Error: {str(e)}")
    
    async def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        template: Optional[str] = None,
        context: Optional[List[int]] = None,
        options: Optional[Dict[str, Any]] = None,
        format: Optional[Union[str, Dict[str, Any]]] = None,
        stream: bool = False
    ) -> Union[Dict[str, Any], AsyncGenerator[Dict[str, Any], None]]:
        """
        Generate text using the Ollama model.
        
        Args:
            model: The model to use for generation
            prompt: The prompt for text generation
            system: Optional system message
            template: Optional template for generation
            context: Optional context for generation
            options: Optional generation options
            format: Optional format for the response
            stream: Whether to stream the response
            
        Returns:
            The Ollama response
            
        Raises:
            OllamaError: If there's an error with the Ollama service
            ModelNotFoundError: If the specified model is not found
        """
        data = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        if system:
            data["system"] = system
        if template:
            data["template"] = template
        if context:
            data["context"] = context
        if options:
            data["options"] = options
        if format:
            data["format"] = format
            
        return await self._make_request("generate", data, stream)
    
    async def chat(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        system: Optional[str] = None,
        template: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        format: Optional[Union[str, Dict[str, Any]]] = None,
        stream: bool = False
    ) -> Union[Dict[str, Any], AsyncGenerator[Dict[str, Any], None]]:
        """
        Chat with the Ollama model.
        
        Args:
            model: The model to use for chat
            messages: The messages for the chat
            system: Optional system message
            template: Optional template for chat
            options: Optional chat options
            format: Optional format for the response
            stream: Whether to stream the response
            
        Returns:
            The Ollama response
            
        Raises:
            OllamaError: If there's an error with the Ollama service
            ModelNotFoundError: If the specified model is not found
        """
        data = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        if system:
            data["system"] = system
        if template:
            data["template"] = template
        if options:
            data["options"] = options
        if format:
            data["format"] = format
            
        return await self._make_request("chat", data, stream)
    
    async def embeddings(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get embeddings from the Ollama model.
        
        Args:
            model: The model to use for embeddings
            prompt: The text to embed
            options: Optional embedding options
            
        Returns:
            The Ollama response containing embeddings
            
        Raises:
            OllamaError: If there's an error with the Ollama service
            ModelNotFoundError: If the specified model is not found
        """
        data = {
            "model": model,
            "prompt": prompt
        }
        
        if options:
            data["options"] = options
            
        return await self._make_request("embeddings", data)
    
    async def show(self, model: str) -> Dict[str, Any]:
        """
        Get information about a model.
        
        Args:
            model: The model name to get information about
            
        Returns:
            The Ollama response containing model information
            
        Raises:
            OllamaError: If there's an error with the Ollama service
            ModelNotFoundError: If the specified model is not found
        """
        data = {
            "name": model
        }
            
        return await self._make_request("show", data)
    
    async def list_models(self) -> Dict[str, Any]:
        """
        List all available models.
        
        Returns:
            The Ollama response containing the list of models
            
        Raises:
            OllamaError: If there's an error with the Ollama service
        """
        return await self._make_request("tags", {})

# Create a singleton instance
ollama_client = OllamaClient() 