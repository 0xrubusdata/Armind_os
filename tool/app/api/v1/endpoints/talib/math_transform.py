from fastapi import APIRouter
from app.models.request.talib_request import TalibRequest
from app.models.response.talib_response import TalibFunctionResult
from .base import create_category_router, talib_endpoint

router = create_category_router("Math Transform")

@router.post(
    "/math/transform/{function_name}",
    response_model=TalibFunctionResult,
    summary="Calculate Math Transform Functions",
    description="""
    Calculate mathematical transformations of price data.
    
    Available functions:
    - ACOS (Vector Trigonometric ACos)
    - ASIN (Vector Trigonometric ASin)
    - ATAN (Vector Trigonometric ATan)
    - CEIL (Vector Ceil)
    - COS (Vector Trigonometric Cos)
    - COSH (Vector Trigonometric Cosh)
    - EXP (Vector Arithmetic Exp)
    - FLOOR (Vector Floor)
    - LN (Vector Log Natural)
    - LOG10 (Vector Log10)
    - SIN (Vector Trigonometric Sin)
    - SINH (Vector Trigonometric Sinh)
    - SQRT (Vector Square Root)
    - TAN (Vector Trigonometric Tan)
    - TANH (Vector Trigonometric Tanh)
    """,
    responses={
        200: {
            "description": "Successful calculation",
            "content": {
                "application/json": {
                    "example": {
                        "function": "SIN",
                        "category": "Math Transform",
                        "results": {
                            "real": [0.0, 0.841, 0.909, 0.141, -0.757]
                        }
                    }
                }
            }
        }
    }
)
@talib_endpoint("Math Transform", "math_transform_functions")
async def calculate_math_transform(
    function_name: str,
    data: TalibRequest
) -> TalibFunctionResult:
    """Calculate a mathematical transformation."""
    pass  # The actual implementation is handled by the decorator 