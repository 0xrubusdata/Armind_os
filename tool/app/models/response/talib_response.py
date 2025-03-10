from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional


class TalibFunctionResult(BaseModel):
    """Base model for TA-Lib function results."""
    function: str = Field(..., description="Name of the TA-Lib function")
    category: str = Field(..., description="Category of the function")
    results: Dict[str, Any] = Field(..., description="Calculation results")


class CategoryInfo(BaseModel):
    """Information about a TA-Lib function category."""
    name: str = Field(..., description="Internal name of the category")
    display_name: str = Field(..., description="Display name of the category")
    description: str = Field(..., description="Description of the category")
    function_count: Optional[int] = Field(None, description="Number of functions in the category")
    endpoint: Optional[str] = Field(None, description="API endpoint for the category functions")


class CategoriesResponse(BaseModel):
    """Response model for the categories endpoint."""
    categories: List[CategoryInfo] = Field(..., description="List of TA-Lib function categories")


class FunctionInfo(BaseModel):
    """Information about a TA-Lib function."""
    name: str = Field(..., description="Name of the function")
    description: str = Field(..., description="Description of the function")
    required_inputs: Dict[str, str] = Field(..., description="Required input parameters")
    optional_inputs: Dict[str, str] = Field(..., description="Optional input parameters")
    endpoint: str = Field(..., description="API endpoint for the function")


class CategoryFunctionsResponse(BaseModel):
    """Response model for the category functions endpoint."""
    category: str = Field(..., description="Category name")
    functions: List[FunctionInfo] = Field(..., description="List of functions in the category")


class FunctionDetailResponse(BaseModel):
    """Response model for the function details endpoint."""
    name: str = Field(..., description="Name of the function")
    category: str = Field(..., description="Category of the function")
    description: str = Field(..., description="Description of the function")
    required_inputs: Dict[str, str] = Field(..., description="Required input parameters")
    optional_inputs: Dict[str, str] = Field(..., description="Optional input parameters")
    endpoint: str = Field(..., description="API endpoint for the function")
    example_request: Dict[str, Any] = Field(..., description="Example request data")


class AllFunctionsResponse(BaseModel):
    """Response model for the all functions endpoint."""
    categories: Dict[str, List[str]] = Field(..., description="Functions grouped by category") 