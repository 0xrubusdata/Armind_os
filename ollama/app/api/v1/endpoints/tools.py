from fastapi import APIRouter, Depends, HTTPException, status, Path
import httpx
import logging
from typing import Dict, Any, List, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tools", tags=["tools"])

# Define available tools
TALIB_TOOL = {
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

@router.get("")
async def list_tools_endpoint():
    """
    List all available tools.
    
    Returns:
        List of available tools
    """
    return {"tools": [TALIB_TOOL]}

@router.get("/{tool_name}")
async def get_tool_endpoint(
    tool_name: str = Path(..., description="The name of the tool to get")
):
    """
    Get details of a specific tool.
    
    Args:
        tool_name: The name of the tool to get
        
    Returns:
        The tool details
    """
    if tool_name == "talib":
        # Get additional information from the TA-Lib API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{settings.TALIB_API_URL}/talib/categories")
                if response.status_code == 200:
                    categories_data = response.json()
                    TALIB_TOOL["categories_detail"] = categories_data
                    
                    # Get functions for each category
                    functions_data = {}
                    for category in TALIB_TOOL["categories"]:
                        category_response = await client.get(f"{settings.TALIB_API_URL}/talib/functions/{category}")
                        if category_response.status_code == 200:
                            functions_data[category] = category_response.json()
                    
                    if functions_data:
                        TALIB_TOOL["functions"] = functions_data
                        
            return TALIB_TOOL
        except Exception as e:
            logger.error(f"Error getting TA-Lib tool details: {str(e)}")
            # Return basic information if API call fails
            return TALIB_TOOL
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool '{tool_name}' not found"
        )

@router.post("/{tool_name}/{endpoint}")
async def execute_tool_endpoint(
    tool_name: str = Path(..., description="The name of the tool to execute"),
    endpoint: str = Path(..., description="The endpoint to call"),
    params: Dict[str, Any] = {}
):
    """
    Execute a tool.
    
    Args:
        tool_name: The name of the tool to execute
        endpoint: The endpoint to call
        params: The parameters to pass to the endpoint
        
    Returns:
        The tool execution result
    """
    try:
        if tool_name == "talib":
            # Construct the full endpoint URL
            if endpoint.startswith("/"):
                endpoint = endpoint[1:]
            full_url = f"{settings.TALIB_API_URL}/{endpoint}"
            
            # Call the TA-Lib API
            async with httpx.AsyncClient() as client:
                response = await client.post(full_url, json=params)
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Error from TA-Lib API: {response.text}"
                    )
                return response.json()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool '{tool_name}' not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing tool: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing tool: {str(e)}"
        ) 