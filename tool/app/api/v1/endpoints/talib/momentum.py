from fastapi import APIRouter, Query, Path
from app.models.request.talib_request import MomentumTalibRequest
from app.models.response.talib_response import TalibFunctionResult
from .base import create_category_router, talib_endpoint
from typing import List

router = create_category_router("Momentum Indicators")

MOMENTUM_FUNCTIONS = {
    "RSI": {
        "description": "Relative Strength Index",
        "parameters": {
            "timeperiod": "Number of periods (default=14)",
        },
        "example": {
            "real": [100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0, 105.0],
            "timeperiod": 14
        }
    },
    "MACD": {
        "description": "Moving Average Convergence/Divergence",
        "parameters": {
            "fastperiod": "Fast period (default=12)",
            "slowperiod": "Slow period (default=26)",
            "signalperiod": "Signal period (default=9)"
        },
        "example": {
            "real": [100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0, 105.0],
            "fastperiod": 12,
            "slowperiod": 26,
            "signalperiod": 9
        }
    }
}

@router.post(
    "/momentum/{function_name}",
    response_model=TalibFunctionResult,
    summary="Calculate Momentum indicators",
    description="""
    Calculate momentum indicators that measure the rate of price changes.
    
    Available functions:
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence/Divergence)
    - STOCH (Stochastic)
    - STOCHF (Stochastic Fast)
    - STOCHRSI (Stochastic Relative Strength Index)
    - ADX (Average Directional Movement Index)
    - ADXR (Average Directional Movement Index Rating)
    - APO (Absolute Price Oscillator)
    - AROON (Aroon)
    - AROONOSC (Aroon Oscillator)
    - BOP (Balance Of Power)
    - CCI (Commodity Channel Index)
    - CMO (Chande Momentum Oscillator)
    - DX (Directional Movement Index)
    - MFI (Money Flow Index)
    - MINUS_DI (Minus Directional Indicator)
    - MINUS_DM (Minus Directional Movement)
    - MOM (Momentum)
    - PLUS_DI (Plus Directional Indicator)
    - PLUS_DM (Plus Directional Movement)
    - PPO (Percentage Price Oscillator)
    - ROC (Rate of change)
    - ROCP (Rate of change Percentage)
    - ROCR (Rate of change ratio)
    - ROCR100 (Rate of change ratio 100 scale)
    - TRIX (1-day Rate-Of-Change of a Triple Smooth EMA)
    - ULTOSC (Ultimate Oscillator)
    - WILLR (Williams' %R)
    
    Each function has specific parameters and requirements. Use the /info endpoint
    to get detailed information about a specific function.
    
    Common parameters:
    - real: List of price values
    - timeperiod: Number of periods for calculation
    
    Notes:
    - Price data should be in chronological order (oldest first)
    - Minimum data points required depends on the function and parameters
    - Some functions may return null values for the initial periods
    """,
    responses={
        200: {
            "description": "Successful calculation",
            "content": {
                "application/json": {
                    "examples": {
                        "RSI": {
                            "summary": "RSI Example",
                            "value": {
                                "function": "RSI",
                                "category": "Momentum Indicators",
                                "results": {
                                    "real": [None, None, None, None, 70.53, 66.32, 66.55]
                                }
                            }
                        },
                        "MACD": {
                            "summary": "MACD Example",
                            "value": {
                                "function": "MACD",
                                "category": "Momentum Indicators",
                                "results": {
                                    "macd": [None, None, None, 0.2, 0.3, -0.1],
                                    "macdsignal": [None, None, None, None, 0.15, 0.1],
                                    "macdhist": [None, None, None, None, 0.15, -0.2]
                                }
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Invalid parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid parameters",
                        "error_code": "INVALID_PARAMETERS",
                        "extra": {
                            "reason": "timeperiod must be greater than 0"
                        }
                    }
                }
            }
        },
        404: {
            "description": "Function not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Function not found",
                        "error_code": "FUNCTION_NOT_FOUND",
                        "extra": {
                            "function_name": "UNKNOWN_FUNC",
                            "available_functions": ["RSI", "MACD", "STOCH", "..."]
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "real"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
@talib_endpoint("Momentum Indicators", "momentum_functions")
async def calculate_momentum(
    function_name: str = Path(
        ..., 
        description="The name of the momentum indicator to calculate",
        example="RSI"
    ),
    data: MomentumTalibRequest = None
) -> TalibFunctionResult:
    """
    Calculate a momentum indicator.
    
    Args:
        function_name: The name of the momentum indicator to calculate
        data: The input data and parameters for the calculation
        
    Returns:
        TalibFunctionResult: The calculated indicator values
        
    Raises:
        HTTPException: If the function is not found or parameters are invalid
    """
    pass  # The actual implementation is handled by the decorator 