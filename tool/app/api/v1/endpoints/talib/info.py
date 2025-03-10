from fastapi import APIRouter, Request
from typing import List

from app.models.response.talib_response import (
    CategoryInfo,
    CategoriesResponse,
    FunctionInfo,
    CategoryFunctionsResponse,
    FunctionDetailResponse,
    AllFunctionsResponse
)
from app.dictionaries.talib.functions.functions_mapping import functions_dictionaries

router = APIRouter()

@router.get(
    "/categories",
    response_model=CategoriesResponse,
    summary="Get all TA-Lib function categories",
    description="Returns a list of all available TA-Lib function categories with their descriptions"
)
async def get_categories(request: Request) -> CategoriesResponse:
    """Get all available TA-Lib function categories."""
    categories = [
        {
            "name": "Overlap Studies",
            "description": "Moving averages and other indicators that overlay price data",
            "links": [{
                "rel": "functions",
                "href": str(request.url_for("get_category_functions", category="overlap")),
                "method": "GET"
            }]
        },
        # Add other categories here...
    ]
    
    return {
        "categories": categories,
        "links": [
            {
                "rel": "self",
                "href": str(request.url),
                "method": "GET"
            },
            {
                "rel": "all_functions",
                "href": str(request.url_for("get_all_functions")),
                "method": "GET"
            }
        ]
    }

@router.get(
    "/functions",
    response_model=AllFunctionsResponse,
    summary="Get all TA-Lib functions",
    description="Returns a list of all available TA-Lib functions with their descriptions"
)
async def get_all_functions() -> AllFunctionsResponse:
    """Get all available TA-Lib functions."""
    functions = []
    for category, funcs in functions_dictionaries.items():
        for func_name, func_info in funcs.items():
            functions.append({
                "name": func_name,
                "category": category,
                "description": func_info.get("description", ""),
                "group": func_info.get("group", "")
            })
    
    return {"functions": functions}

@router.get(
    "/function/{function_name}",
    response_model=FunctionDetailResponse,
    summary="Get details for a specific TA-Lib function",
    description="Returns detailed information about a specific TA-Lib function"
)
async def get_function_details(function_name: str) -> FunctionDetailResponse:
    """Get detailed information about a specific TA-Lib function."""
    for category, funcs in functions_dictionaries.items():
        if function_name in funcs:
            func_info = funcs[function_name]
            return {
                "name": function_name,
                "category": category,
                "description": func_info.get("description", ""),
                "group": func_info.get("group", ""),
                "parameters": func_info.get("parameters", {}),
                "outputs": func_info.get("outputs", {}),
                "example_inputs": func_info.get("example_inputs", {})
            }
    
    raise HTTPException(status_code=404, detail=f"Function {function_name} not found") 