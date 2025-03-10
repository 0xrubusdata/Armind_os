from typing import Dict, Any, Optional, List
import httpx
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.core.config import settings
from app.core.exceptions import ToolError, ToolNotFoundError, ToolTimeoutError

logger = logging.getLogger(__name__)

class ToolClient:
    """Client for interacting with external tools."""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the tool client.
        
        Args:
            base_url: The base URL for the tool API. If not provided, uses the URL from settings.
        """
        self.base_url = base_url or settings.TALIB_API_URL
        self.timeout = httpx.Timeout(30.0, connect=5.0)
        self.limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True
    )
    async def _make_request(
        self, 
        method: str,
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a request to the tool API.
        
        Args:
            method: The HTTP method to use
            endpoint: The API endpoint to call
            data: The data to send in the request body
            params: The query parameters to send
            
        Returns:
            The response from the tool API
            
        Raises:
            ToolError: If there's an error calling the API
            ToolNotFoundError: If the specified tool or endpoint is not found
            ToolTimeoutError: If the request times out
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout, limits=self.limits) as client:
                if method.upper() == "GET":
                    response = await client.get(url, params=params)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data)
                else:
                    raise ToolError(f"Unsupported HTTP method: {method}")
                    
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error calling tool API: {str(e)}")
            if e.response.status_code == 404:
                raise ToolNotFoundError(f"Tool or endpoint not found: {endpoint}")
            raise ToolError(f"HTTP error: {str(e)}")
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error calling tool API: {str(e)}")
            raise ToolTimeoutError(f"Request timed out: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error calling tool API: {str(e)}")
            raise ToolError(f"Request error: {str(e)}")
        except Exception as e:
            logger.error(f"Error calling tool API: {str(e)}")
            raise ToolError(f"Error: {str(e)}")
    
    async def get_categories(self) -> Dict[str, Any]:
        """
        Get all TA-Lib function categories.
        
        Returns:
            The TA-Lib categories
            
        Raises:
            ToolError: If there's an error with the TA-Lib API
            ToolNotFoundError: If the categories endpoint is not found
            ToolTimeoutError: If the request times out
        """
        return await self._make_request("GET", "talib/categories")
    
    async def get_functions(self, category: str) -> Dict[str, Any]:
        """
        Get all functions for a specific category.
        
        Args:
            category: The category to get functions for
            
        Returns:
            The TA-Lib functions for the category
            
        Raises:
            ToolError: If there's an error with the TA-Lib API
            ToolNotFoundError: If the category is not found
            ToolTimeoutError: If the request times out
        """
        return await self._make_request("GET", f"talib/functions/{category}")
    
    async def get_function_details(self, function_name: str) -> Dict[str, Any]:
        """
        Get details for a specific function.
        
        Args:
            function_name: The function name to get details for
            
        Returns:
            The TA-Lib function details
            
        Raises:
            ToolError: If there's an error with the TA-Lib API
            ToolNotFoundError: If the function is not found
            ToolTimeoutError: If the request times out
        """
        return await self._make_request("GET", f"talib/function/{function_name}")
    
    async def execute_function(
        self,
        category: str,
        function_name: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a TA-Lib function.
        
        Args:
            category: The category of the function
            function_name: The function name to execute
            data: The data to pass to the function
            
        Returns:
            The TA-Lib function result
            
        Raises:
            ToolError: If there's an error with the TA-Lib API
            ToolNotFoundError: If the function is not found
            ToolTimeoutError: If the request times out
        """
        return await self._make_request("POST", f"talib/{category}/{function_name}", data=data)
    
    async def execute_tool(
        self,
        tool_name: str,
        endpoint: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool.
        
        Args:
            tool_name: The name of the tool to execute
            endpoint: The endpoint to call
            params: The parameters to pass to the endpoint
            
        Returns:
            The tool execution result
            
        Raises:
            ToolError: If there's an error executing the tool
            ToolNotFoundError: If the tool or endpoint is not found
            ToolTimeoutError: If the request times out
        """
        if tool_name == "talib":
            # Construct the full endpoint URL
            if endpoint.startswith("/"):
                endpoint = endpoint[1:]
                
            return await self._make_request("POST", endpoint, data=params)
        else:
            raise ToolNotFoundError(f"Unknown tool: {tool_name}")

# Create a singleton instance
tool_client = ToolClient() 