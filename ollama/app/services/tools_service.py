from typing import Dict, Any, List
import logging

from app.core.logging import logger
from app.core.config import settings
from app.services.base_service import BaseService
from app.utils.tool_client import tool_client

logger = logging.getLogger(__name__)

class ToolsService(BaseService):
    """Service for handling tool-related operations."""

    async def list_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        List all available tools.
        
        Returns:
            A dictionary containing the list of available tools
        """
        try:
            await self.log_request("list_tools")
            
            # Define available tools
            talib_tool = {
                "name": "talib",
                "description": "Technical Analysis Library for financial market data",
                "api_url": settings.TALIB_API_URL,
                "capabilities": [
                    "Calculate technical indicators for financial data",
                    "Analyze price patterns",
                    "Compute statistical measures for time series data"
                ],
                "categories": [
                    "momentum", "volume", "volatility", "price", 
                    "cycle", "pattern", "statistic", "math_transform", "math_operator"
                ]
            }
            
            return {"tools": [talib_tool]}
        except Exception as e:
            logger.error(f"Error listing tools: {str(e)}")
            raise
    
    async def get_tool(self, tool_name: str) -> Dict[str, Any]:
        """
        Get details of a specific tool.
        
        Args:
            tool_name: The name of the tool to get
            
        Returns:
            The tool details
            
        Raises:
            OllamaError: If the tool is not found
        """
        try:
            await self.log_request("get_tool", tool_name=tool_name)
            
            if tool_name == "talib":
                # Define the tool
                talib_tool = {
                    "name": "talib",
                    "description": "Technical Analysis Library for financial market data",
                    "api_url": settings.TALIB_API_URL,
                    "capabilities": [
                        "Calculate technical indicators for financial data",
                        "Analyze price patterns",
                        "Compute statistical measures for time series data"
                    ],
                    "categories": [
                        "momentum", "volume", "volatility", "price", 
                        "cycle", "pattern", "statistic", "math_transform", "math_operator"
                    ]
                }
                
                # Get additional information from the TA-Lib API
                try:
                    # Get categories
                    categories_data = await tool_client.get_categories()
                    talib_tool["categories_detail"] = categories_data
                    
                    # Get functions for each category
                    functions_data = {}
                    for category in talib_tool["categories"]:
                        category_functions = await tool_client.get_functions(category)
                        functions_data[category] = category_functions
                    
                    if functions_data:
                        talib_tool["functions"] = functions_data
                except Exception as e:
                    logger.error(f"Error getting TA-Lib tool details: {str(e)}")
                
                return talib_tool
            else:
                raise ValueError(f"Tool '{tool_name}' not found")
        except ValueError as e:
            logger.error(f"Error getting tool: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error getting tool: {str(e)}")
            raise
    
    async def execute_tool_endpoint(self, tool_name: str, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool.
        
        Args:
            tool_name: The name of the tool to execute
            endpoint: The endpoint to call
            params: The parameters to pass to the endpoint
            
        Returns:
            The tool execution result
            
        Raises:
            OllamaError: If there's an error executing the tool
        """
        try:
            await self.log_request("execute_tool", tool_name=tool_name, endpoint=endpoint)
            return await self.execute_tool(tool_name, endpoint, params)
        except Exception as e:
            logger.error(f"Error executing tool: {str(e)}")
            raise
