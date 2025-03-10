from pydantic import BaseModel, Field
from typing import List, Optional

class ShowSyncModelDetails(BaseModel):
    """
    Model details response from show endpoint.
    """
    parent_model: Optional[str] = Field(None, description="Parent model name")
    format: Optional[str] = Field(None, description="Model format")
    family: Optional[str] = Field(None, description="Model family")
    families: Optional[List[str]] = Field(None, description="List of model families")
    parameter_size: Optional[str] = Field(None, description="Model parameter size")
    quantization_level: Optional[str] = Field(None, description="Model quantization level")

class ShowSyncCompleteResponse(BaseModel):
    """
    Complete response model for model information.
    """
    model: str = Field(..., description="Model name")
    details: ShowSyncModelDetails = Field(..., description="Model details")
    template: Optional[str] = Field(None, description="Model template")
    license: Optional[str] = Field(None, description="Model license")
    system: Optional[str] = Field(None, description="Model system message")
    