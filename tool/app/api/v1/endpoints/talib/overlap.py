from fastapi import APIRouter
from app.models.request.talib_request import OverlapTalibRequest
from app.models.response.talib_response import TalibFunctionResult
from .base import create_category_router, talib_endpoint

router = create_category_router("Overlap Studies")

@router.post(
    "/overlap/{function_name}",
    response_model=TalibFunctionResult,
    summary="Calculate Overlap Studies indicators",
    description="""
    Calculate indicators that overlay price data, such as moving averages.
    
    Available functions:
    - SMA (Simple Moving Average)
    - EMA (Exponential Moving Average)
    - WMA (Weighted Moving Average)
    - DEMA (Double Exponential Moving Average)
    - TEMA (Triple Exponential Moving Average)
    - TRIMA (Triangular Moving Average)
    - KAMA (Kaufman Adaptive Moving Average)
    - MAMA (MESA Adaptive Moving Average)
    - T3 (Triple Exponential Moving Average)
    - BBANDS (Bollinger Bands)
    - MIDPOINT (Midpoint Price over period)
    - MIDPRICE (Midpoint Price over period)
    - SAR (Parabolic SAR)
    - SAREXT (Parabolic SAR - Extended)
    - HT_TRENDLINE (Hilbert Transform - Instantaneous Trendline)
    """,
    responses={
        200: {
            "description": "Successful calculation",
            "content": {
                "application/json": {
                    "example": {
                        "function": "SMA",
                        "category": "Overlap Studies",
                        "results": {
                            "real": [None, None, None, None, 102.5, 103.5, 104.5]
                        }
                    }
                }
            }
        }
    }
)
@talib_endpoint("Overlap Studies", "overlap_functions")
async def calculate_overlap(
    function_name: str,
    data: OverlapTalibRequest
) -> TalibFunctionResult:
    """Calculate an overlap studies indicator."""
    pass  # The actual implementation is handled by the decorator 