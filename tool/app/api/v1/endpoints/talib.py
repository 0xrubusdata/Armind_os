from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Callable, List
from functools import wraps

from app.models.request.talib_request import (
    MathOperatorTalibRequest, 
    MomentumTalibRequest, 
    OverlapTalibRequest, 
    PatternTalibRequest, 
    PriceTalibRequest, 
    StatisticTalibRequest, 
    TalibRequest, 
    VolatilityTalibRequest,
    VolumeTalibRequest
)
from app.models.response.talib_response import (
    TalibFunctionResult,
    CategoryInfo,
    CategoriesResponse,
    FunctionInfo,
    CategoryFunctionsResponse,
    FunctionDetailResponse,
    AllFunctionsResponse
)
from app.services.talib_service import TalibService
from app.api.deps import get_talib_service, TalibServiceDep
from app.core.logging import logger
from app.models.dto.talib_dto_factory import TalibDtoFactory
from app.dictionaries.talib.functions.functions_mapping import functions_dictionaries
from app.core.exceptions import (
    AppException,
    TalibException,
    FunctionNotFoundException,
    CategoryNotFoundException,
    InvalidParameterException,
    CalculationException
)


router = APIRouter(prefix="/talib", tags=["talib"])

# Define a decorator to handle common endpoint logic
def talib_endpoint(category: str, dictionary_name: str):
    """
    Decorator for TA-Lib endpoints to reduce code duplication.
    
    Args:
        category: Human-readable category name
        dictionary_name: Dictionary name for function lookup
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(function_name: str, data, talib_service: TalibService = Depends(get_talib_service)):
            try:
                logger.info(f"Processing {category} function: {function_name}")
                talib_dto = TalibDtoFactory.build(function_name, dictionary_name, data)
                result = await talib_service.process_talib_request(function_name, talib_dto, category)
                logger.info(f"Successfully processed {category} function: {function_name}")
                return result
            except AppException as e:
                # Re-raise application exceptions
                logger.warning(f"Application error in {category} function {function_name}: {e.detail}")
                raise e
            except Exception as e:
                # Log and convert other exceptions to CalculationException
                logger.error(f"Unexpected error in {category} function {function_name}: {str(e)}", exc_info=True)
                raise CalculationException(function_name, str(e))
        return wrapper
    return decorator


@router.post("/overlap/{function_name}", summary="Calculate Overlap Studies indicators", response_model=TalibFunctionResult)
@talib_endpoint("Overlap Studies", "overlap_functions")
async def calculate_overlap(
    function_name: str,
    data: OverlapTalibRequest,
    talib_service: TalibService = Depends(get_talib_service)
):
    """
    Calculate Overlap Studies indicators.
    
    These functions include moving averages and other indicators that overlay price data.
    
    Examples: SMA, EMA, BBANDS, etc.
    """
    pass  # Implementation handled by decorator


@router.post("/momentum/{function_name}", summary="Calculate Momentum indicators", response_model=TalibFunctionResult)
@talib_endpoint("Momentum Indicators", "momentum_functions")
async def calculate_momentum(
    function_name: str,
    data: MomentumTalibRequest,
    talib_service: TalibService = Depends(get_talib_service)
):
    """
    Calculate Momentum indicators.
    
    These functions measure the rate of price changes.
    
    Examples: RSI, MACD, Stochastic, etc.
    """
    pass  # Implementation handled by decorator


@router.post("/volume/{function_name}", summary="Calculate Volume indicators", response_model=TalibFunctionResult)
@talib_endpoint("Volume Indicators", "volume_functions")
async def calculate_volume(
    function_name: str,
    data: VolumeTalibRequest,
    talib_service: TalibService = Depends(get_talib_service)
):
    """
    Calculate Volume indicators.
    
    These functions analyze trading volume.
    
    Examples: OBV, AD, etc.
    """
    pass  # Implementation handled by decorator


@router.post("/volatility/{function_name}", summary="Calculate Volatility indicators", response_model=TalibFunctionResult)
@talib_endpoint("Volatility Indicators", "volatility_functions")
async def calculate_volatility(
    function_name: str,
    data: VolatilityTalibRequest,
    talib_service: TalibService = Depends(get_talib_service)
):
    """
    Calculate Volatility indicators.
    
    These functions measure the rate of price movement.
    
    Examples: ATR, NATR, etc.
    """
    pass  # Implementation handled by decorator


@router.post("/price/{function_name}", summary="Calculate Price Transform indicators", response_model=TalibFunctionResult)
@talib_endpoint("Price Transform", "price_functions")
async def calculate_price(
    function_name: str,
    data: PriceTalibRequest,
    talib_service: TalibService = Depends(get_talib_service)
):
    """
    Calculate Price Transform indicators.
    
    These functions transform price data.
    
    Examples: AVGPRICE, MEDPRICE, etc.
    """
    pass  # Implementation handled by decorator


@router.post("/cycle/{function_name}", summary="Calculate Cycle indicators", response_model=TalibFunctionResult)
@talib_endpoint("Cycle Indicators", "cycle_functions")
async def calculate_cycle(
    function_name: str,
    data: TalibRequest,
    talib_service: TalibService = Depends(get_talib_service)
):
    """
    Calculate Cycle indicators.
    
    These functions identify cycles in price data.
    
    Examples: HT_DCPERIOD, HT_PHASOR, etc.
    """
    pass  # Implementation handled by decorator


@router.post("/pattern/{function_name}", summary="Calculate Pattern Recognition indicators", response_model=TalibFunctionResult)
@talib_endpoint("Pattern Recognition", "pattern_functions")
async def calculate_pattern(
    function_name: str,
    data: PatternTalibRequest,
    talib_service: TalibService = Depends(get_talib_service)
):
    """
    Calculate Pattern Recognition indicators.
    
    These functions identify patterns in price data.
    
    Examples: CDLDOJI, CDLENGULFING, etc.
    """
    pass  # Implementation handled by decorator


@router.post("/statistic/{function_name}", summary="Calculate Statistic Functions", response_model=TalibFunctionResult)
@talib_endpoint("Statistic Functions", "statistic_functions")
async def calculate_statistic(
    function_name: str,
    data: StatisticTalibRequest,
    talib_service: TalibService = Depends(get_talib_service)
):
    """
    Calculate Statistic Functions.
    
    These functions perform statistical calculations.
    
    Examples: BETA, CORREL, etc.
    """
    pass  # Implementation handled by decorator


@router.post("/math/transform/{function_name}", summary="Calculate Math Transform Functions", response_model=TalibFunctionResult)
@talib_endpoint("Math Transform", "math_transform_functions")
async def calculate_math_transform(
    function_name: str,
    data: TalibRequest,
    talib_service: TalibService = Depends(get_talib_service)
):
    """
    Calculate Math Transform Functions.
    
    These functions perform mathematical transformations.
    
    Examples: SIN, COS, etc.
    """
    pass  # Implementation handled by decorator


@router.post("/math/operator/{function_name}", summary="Calculate Math Operator Functions", response_model=TalibFunctionResult)
@talib_endpoint("Math Operators", "math_operator_functions")
async def calculate_math_operator(
    function_name: str,
    data: MathOperatorTalibRequest,
    talib_service: TalibService = Depends(get_talib_service)
):
    """
    Calculate Math Operator Functions.
    
    These functions perform mathematical operations.
    
    Examples: ADD, SUB, etc.
    """
    pass  # Implementation handled by decorator


@router.get("/categories", summary="Get all TA-Lib function categories", response_model=CategoriesResponse)
async def get_categories():
    """
    Get a list of all available TA-Lib function categories.
    
    Returns a list of category names and their descriptions.
    """
    categories = [
        {"name": "overlap_functions", "display_name": "Overlap Studies", "description": "Moving averages and other indicators that overlay price data"},
        {"name": "momentum_functions", "display_name": "Momentum Indicators", "description": "Indicators that measure the rate of price changes"},
        {"name": "volume_functions", "display_name": "Volume Indicators", "description": "Indicators that analyze trading volume"},
        {"name": "volatility_functions", "display_name": "Volatility Indicators", "description": "Indicators that measure the rate of price movement"},
        {"name": "price_functions", "display_name": "Price Transform", "description": "Functions that transform price data"},
        {"name": "cycle_functions", "display_name": "Cycle Indicators", "description": "Indicators that identify cycles in price data"},
        {"name": "pattern_functions", "display_name": "Pattern Recognition", "description": "Indicators that identify patterns in price data"},
        {"name": "statistic_functions", "display_name": "Statistic Functions", "description": "Statistical calculations on price data"},
        {"name": "math_transform_functions", "display_name": "Math Transform", "description": "Mathematical transformations of price data"},
        {"name": "math_operator_functions", "display_name": "Math Operators", "description": "Mathematical operations on price data"}
    ]
    
    # Add function count to each category
    for category in categories:
        category_name = category["name"]
        if category_name in functions_dictionaries:
            category["function_count"] = len(functions_dictionaries[category_name])
            category["endpoint"] = f"/api/v1/talib/functions/{category_name}"
    
    return {
        "categories": categories
    }


@router.get("/functions", summary="Get all available TA-Lib functions", response_model=AllFunctionsResponse)
async def get_all_functions():
    """
    Get a list of all available TA-Lib functions grouped by category.
    
    Returns a dictionary with categories as keys and lists of function names as values.
    """
    result = {}
    for category, functions in functions_dictionaries.items():
        result[category] = list(functions.keys())
    
    return {
        "categories": result
    }


@router.get("/functions/{category}", summary="Get functions for a specific category", response_model=CategoryFunctionsResponse)
async def get_category_functions(category: str):
    """
    Get detailed information about all functions in a specific category.
    
    Args:
        category: The category name (e.g., 'overlap_functions')
        
    Returns:
        A list of functions with their details
    """
    if category not in functions_dictionaries:
        raise CategoryNotFoundException(category)
    
    functions = functions_dictionaries[category]
    result = []
    
    for function_name, function_data in functions.items():
        # Get required inputs
        inputs = function_data.get("inputs", {})
        required_inputs = {}
        optional_inputs = {}
        
        for input_name, default_value in inputs.items():
            if default_value is None:
                required_inputs[input_name] = "Required"
            else:
                optional_inputs[input_name] = f"Optional (default: {default_value})"
        
        # Create function info
        function_info = {
            "name": function_name,
            "description": function_data.get("description", f"TA-Lib {function_name} function"),
            "required_inputs": required_inputs,
            "optional_inputs": optional_inputs,
            "endpoint": f"/api/v1/talib/{category.replace('_functions', '')}/{function_name}"
        }
        
        result.append(function_info)
    
    return {
        "category": category,
        "functions": result
    }


@router.get("/function/{function_name}", summary="Get details for a specific function", response_model=FunctionDetailResponse)
async def get_function_details(function_name: str):
    """
    Get detailed information about a specific TA-Lib function.
    
    Args:
        function_name: The name of the function (e.g., 'SMA')
        
    Returns:
        Detailed information about the function
    """
    # Find the function in all categories
    for category, functions in functions_dictionaries.items():
        if function_name in functions:
            function_data = functions[function_name]
            
            # Get required inputs
            inputs = function_data.get("inputs", {})
            required_inputs = {}
            optional_inputs = {}
            
            for input_name, default_value in inputs.items():
                if default_value is None:
                    required_inputs[input_name] = "Required"
                else:
                    optional_inputs[input_name] = f"Optional (default: {default_value})"
            
            # Create function info
            function_info = {
                "name": function_name,
                "category": category,
                "description": function_data.get("description", f"TA-Lib {function_name} function"),
                "required_inputs": required_inputs,
                "optional_inputs": optional_inputs,
                "endpoint": f"/api/v1/talib/{category.replace('_functions', '')}/{function_name}"
            }
            
            # Add example request
            example_request = {}
            for input_name in required_inputs:
                if input_name in ["high", "low", "close", "open", "volume"]:
                    example_request[input_name] = [100.0, 101.0, 102.0, 101.5, 103.0]
                elif input_name in ["real", "real0", "real1"]:
                    example_request[input_name] = [100.0, 101.0, 102.0, 101.5, 103.0]
                elif "period" in input_name:
                    example_request[input_name] = 14
                else:
                    example_request[input_name] = 0
            
            function_info["example_request"] = example_request
            
            return function_info
    
    # If function not found
    raise FunctionNotFoundException(function_name)