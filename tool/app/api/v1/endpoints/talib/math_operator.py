from fastapi import APIRouter
from app.models.request.talib_request import MathOperatorTalibRequest
from app.models.response.talib_response import TalibFunctionResult
from .base import create_category_router, talib_endpoint

router = create_category_router("Math Operators")

@router.post(
    "/math/operator/{function_name}",
    response_model=TalibFunctionResult,
    summary="Calculate Math Operator Functions",
    description="""
    Calculate mathematical operations on price data.
    
    Available functions:
    - ADD (Vector Arithmetic Add)
    - DIV (Vector Arithmetic Div)
    - MAX (Highest value over a specified period)
    - MAXINDEX (Index of highest value over a specified period)
    - MIN (Lowest value over a specified period)
    - MININDEX (Index of lowest value over a specified period)
    - MINMAX (Lowest and highest values over a specified period)
    - MINMAXINDEX (Indexes of lowest and highest values over a specified period)
    - MULT (Vector Arithmetic Mult)
    - SUB (Vector Arithmetic Subtraction)
    - SUM (Summation)
    """,
    responses={
        200: {
            "description": "Successful calculation",
            "content": {
                "application/json": {
                    "example": {
                        "function": "ADD",
                        "category": "Math Operators",
                        "results": {
                            "real": [101.0, 103.0, 105.0, 104.5, 107.0]
                        }
                    }
                }
            }
        }
    }
)
@talib_endpoint("Math Operators", "math_operator_functions")
async def calculate_math_operator(
    function_name: str,
    data: MathOperatorTalibRequest
) -> TalibFunctionResult:
    """Calculate a mathematical operation."""
    pass  # The actual implementation is handled by the decorator 