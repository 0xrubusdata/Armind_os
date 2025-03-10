import talib
import numpy as np
from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException
from typing import Dict, Any
from app.core.logging import logger

from app.utils.talib_runner import talib_abstract
from app.models.dto.talib_dto_factory import TalibDto
from app.core.exceptions import CalculationException, FunctionNotFoundException
from app.core.cache import cache_result
from app.core.metrics import CALCULATION_TIME, CACHE_HITS, CACHE_MISSES

class TalibService:
    """Service for handling TA-Lib calculations."""
    
    @cache_result()
    async def calculate(
        self,
        function_name: str,
        real: Optional[List[float]] = None,
        high: Optional[List[float]] = None,
        low: Optional[List[float]] = None,
        close: Optional[List[float]] = None,
        volume: Optional[List[float]] = None,
        open: Optional[List[float]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate a TA-Lib function with the given parameters.
        
        Args:
            function_name: Name of the TA-Lib function to calculate
            real: List of price values for single-input functions
            high: List of high prices
            low: List of low prices
            close: List of closing prices
            volume: List of volume values
            open: List of opening prices
            **kwargs: Additional parameters for the function
            
        Returns:
            Dict containing the calculation results
            
        Raises:
            FunctionNotFoundException: If the function doesn't exist
            CalculationException: If there's an error during calculation
        """
        try:
            # Get the function from TA-Lib
            func = getattr(talib, function_name, None)
            if func is None:
                raise FunctionNotFoundException(f"Function {function_name} not found")
            
            # Convert inputs to numpy arrays
            inputs = {}
            if real is not None:
                inputs["real"] = np.array(real, dtype=np.float64)
            if high is not None:
                inputs["high"] = np.array(high, dtype=np.float64)
            if low is not None:
                inputs["low"] = np.array(low, dtype=np.float64)
            if close is not None:
                inputs["close"] = np.array(close, dtype=np.float64)
            if volume is not None:
                inputs["volume"] = np.array(volume, dtype=np.float64)
            if open is not None:
                inputs["open"] = np.array(open, dtype=np.float64)
            
            # Calculate with timing
            with CALCULATION_TIME.time():
                result = func(**inputs, **kwargs)
            
            # Convert result to dictionary
            if isinstance(result, tuple):
                # Multiple outputs
                output = {}
                for i, value in enumerate(result):
                    output[f"output{i+1}"] = value.tolist()
            else:
                # Single output
                output = {"real": result.tolist()}
            
            return {
                "function": function_name,
                "results": output
            }
            
        except AttributeError as e:
            raise FunctionNotFoundException(f"Function {function_name} not found")
        except Exception as e:
            logger.error(f"Error calculating {function_name}: {str(e)}")
            raise CalculationException(f"Error calculating {function_name}: {str(e)}")

    async def process_talib_request(
        self,
        function_name: str,
        talib_dto: TalibDto,
        category: str
    ) -> Dict[str, Any]:
        """
        Generic function to process TA-Lib requests.
        
        Args:
            function_name: Name of the TA-Lib function to call
            talib_dto: Input talib_dto for the function
            category: Category of the function
            
        Returns:
            The calculation results
            
        Raises:
            CalculationException: If there's an error during calculation
        """
        try:
            results = await talib_abstract(
                        function_name,
                        talib_dto
                    )
            return {
                "function": function_name,
                "category": category,
                "results": results
            }

        except Exception as e:
            logger.error(f"Error processing {category} function {function_name}: {str(e)}")
            if isinstance(e, CalculationException):
                raise e
            else:
                raise CalculationException(function_name, str(e))

