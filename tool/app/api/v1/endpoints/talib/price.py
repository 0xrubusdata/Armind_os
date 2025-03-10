from fastapi import APIRouter
from app.models.request.talib_request import PriceTalibRequest
from app.models.response.talib_response import TalibFunctionResult
from .base import create_category_router, talib_endpoint

router = create_category_router("Price Transform")

@router.post(
    "/price/{function_name}",
    response_model=TalibFunctionResult,
    summary="Calculate Price Transform indicators",
    description="""
    Calculate functions that transform price data.
    
    Available functions:
    - AVGPRICE (Average Price)
    - MEDPRICE (Median Price)
    - TYPPRICE (Typical Price)
    - WCLPRICE (Weighted Close Price)
    """,
    responses={
        200: {
            "description": "Successful calculation",
            "content": {
                "application/json": {
                    "example": {
                        "function": "AVGPRICE",
                        "category": "Price Transform",
                        "results": {
                            "real": [100.25, 101.50, 102.75, 101.25, 103.50]
                        }
                    }
                }
            }
        }
    }
)
@talib_endpoint("Price Transform", "price_functions")
async def calculate_price(
    function_name: str,
    data: PriceTalibRequest
) -> TalibFunctionResult:
    """Calculate a price transform indicator."""
    pass  # The actual implementation is handled by the decorator 