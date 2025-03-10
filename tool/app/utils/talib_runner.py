import talib
import numpy as np
from fastapi import HTTPException
from app.core.logging import logger
from app.models.dto.talib_dto_factory import TalibDto
from app.core.exceptions import CalculationException

async def talib_abstract(function_name: str, talib_dto: TalibDto) -> dict:
    """
    Execute a TA-Lib function with the provided parameters.
    
    Args:
        function_name: Name of the TA-Lib function to call
        talib_dto: Data transfer object containing the parameters
        
    Returns:
        Dictionary with the calculation results
        
    Raises:
        CalculationException: If there's an error during calculation
    """
    try:
        # Convert DTO attributes to NumPy arrays
        talib_dto_dict = talib_dto.dict()
        for key, value in talib_dto_dict.items():
            if isinstance(value, list):
                talib_dto_dict[key] = np.array(value)

        # Get the TA-Lib function and execute it
        function = talib.abstract.Function(function_name)
        results = function(talib_dto_dict)
        
        # Convert NumPy arrays to lists for JSON serialization
        if isinstance(results, np.ndarray):
            results = results.tolist()
        elif isinstance(results, dict):
            for key, value in results.items():
                if isinstance(value, np.ndarray):
                    results[key] = value.tolist()
                    
        return results
    except Exception as e:
        logger.error(f"Error executing TA-Lib function {function_name}: {str(e)}")
        raise CalculationException(function_name, str(e))
