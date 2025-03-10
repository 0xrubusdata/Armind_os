from fastapi import HTTPException
from app.models.request.talib_request import TalibRequest
from pydantic import BaseModel
from typing import Dict, Any, Type

from app.dictionaries.talib.dto.dto_mapping import dto_dictionaries
from app.dictionaries.talib.functions.functions_mapping import functions_dictionaries
from app.dictionaries.talib.dto.basic_dto import TalibDto
from app.core.logging import logger
from app.core.exceptions import (
    CategoryNotFoundException,
    FunctionNotFoundException,
    InvalidParameterException
)

class TalibDtoFactory(BaseModel):
    @staticmethod
    def build(function_name: str, dictionary_name: str, talib_request: TalibRequest) -> TalibDto:
        """
        Build a DTO for the specified TA-Lib function.
        
        Args:
            function_name: Name of the TA-Lib function
            dictionary_name: Category of the function (e.g., 'overlap_functions')
            talib_request: Request data containing the parameters
            
        Returns:
            A TalibDto object with the appropriate parameters
            
        Raises:
            CategoryNotFoundException: If the dictionary is not found
            FunctionNotFoundException: If the function is not found in the dictionary
            InvalidParameterException: If required parameters are missing or invalid
        """
        # Validate dictionary exists
        if dictionary_name not in functions_dictionaries:
            logger.error(f"Dictionary '{dictionary_name}' not found")
            raise CategoryNotFoundException(dictionary_name)

        selected_dictionary = functions_dictionaries[dictionary_name]

        # Validate function exists in dictionary
        if function_name not in selected_dictionary:
            logger.error(f"Function '{function_name}' not found in '{dictionary_name}'")
            raise FunctionNotFoundException(function_name, dictionary_name)

        # Get function data and validate required inputs
        function_data = selected_dictionary[function_name]
        required_inputs = function_data.get("inputs", {})
        request_data = talib_request.dict(exclude_unset=True)
        
        missing_inputs = []
        for input_name, default_value in required_inputs.items():
            if input_name not in request_data and default_value is None:
                missing_inputs.append(input_name)
        
        if missing_inputs:
            logger.error(f"Missing required inputs for function '{function_name}': {missing_inputs}")
            raise InvalidParameterException(function_name, missing_inputs=missing_inputs)

        # Transform request to DTO
        try:
            if function_name in dto_dictionaries[dictionary_name]:
                dto_class = dto_dictionaries[dictionary_name][function_name]
                return dto_class(**request_data)
            else:
                logger.error(f"No DTO found for function '{function_name}'")
                raise FunctionNotFoundException(
                    function_name, 
                    dictionary_name
                )
        except Exception as e:
            logger.error(f"Error creating DTO for function '{function_name}': {str(e)}")
            raise InvalidParameterException(
                function_name, 
                invalid_params={"error": str(e)}
            )
