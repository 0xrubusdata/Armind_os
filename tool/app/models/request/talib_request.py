from pydantic import BaseModel, Field, validator, conlist
from typing import List, Optional, Union
import numpy as np


class TalibRequest(BaseModel):
    """Base class for all TA-Lib requests."""
    real: List[float] = Field(
        ...,
        description="List of price values",
        example=[100.0, 101.0, 102.0, 101.5, 103.0],
        min_items=2,
        max_items=100000
    )

    @validator('real')
    def validate_real(cls, v):
        if not v:
            raise ValueError("Price data cannot be empty")
        if any(not isinstance(x, (int, float)) or np.isnan(x) or np.isinf(x) for x in v):
            raise ValueError("Price data must contain only valid numbers")
        return v

    class Config:
        schema_extra = {
            "example": {
                "real": [100.0, 101.0, 102.0, 101.5, 103.0]
            }
        }

class OverlapTalibRequest(TalibRequest):
    """Request model for Overlap Studies functions."""
    timeperiod: Optional[int] = Field(None, description="Number of periods")
    nbdevup: Optional[float] = Field(None, description="Upper deviation multiplier")
    nbdevdn: Optional[float] = Field(None, description="Lower deviation multiplier")
    matype: Optional[int] = Field(None, description="Moving average type")
    fastlimit: Optional[float] = Field(None, description="Fast limit")
    slowlimit: Optional[float] = Field(None, description="Slow limit")
    periods: Optional[List[int]] = Field(None, description="List of periods")
    minperiod: Optional[int] = Field(None, description="Minimum period")
    maxperiod: Optional[int] = Field(None, description="Maximum period")
    high: Optional[List[float]] = Field(None, description="High price series")
    low: Optional[List[float]] = Field(None, description="Low price series")
    close: Optional[List[float]] = Field(None, description="Close price series")
    acceleration: Optional[float] = Field(None, description="Acceleration factor")
    maximum: Optional[float] = Field(None, description="Maximum value")
    startvalue: Optional[float] = Field(None, description="Start value")
    offsetonreverse: Optional[bool] = Field(None, description="Offset on reverse")
    accelerationinitlong: Optional[float] = Field(None, description="Initial acceleration for long")
    accelerationlong: Optional[float] = Field(None, description="Acceleration for long")
    accelerationmaxlong: Optional[float] = Field(None, description="Maximum acceleration for long")
    accelerationinitshor: Optional[float] = Field(None, description="Initial acceleration for short")
    accelerationshort: Optional[float] = Field(None, description="Acceleration for short")
    accelerationmaxshort: Optional[float] = Field(None, description="Maximum acceleration for short")
    vfactor: Optional[float] = Field(None, description="Volume factor")

class MomentumTalibRequest(TalibRequest):
    """Request model for momentum indicators."""
    timeperiod: Optional[int] = Field(
        None,
        description="Number of periods",
        ge=1,
        le=100000,
        example=14
    )
    fastperiod: Optional[int] = Field(
        None,
        description="Fast period for MACD",
        ge=1,
        le=100000,
        example=12
    )
    slowperiod: Optional[int] = Field(
        None,
        description="Slow period for MACD",
        ge=1,
        le=100000,
        example=26
    )
    signalperiod: Optional[int] = Field(
        None,
        description="Signal period for MACD",
        ge=1,
        le=100000,
        example=9
    )

    @validator('slowperiod')
    def validate_slowperiod(cls, v, values):
        if v is not None and 'fastperiod' in values and values['fastperiod'] is not None:
            if v <= values['fastperiod']:
                raise ValueError("slowperiod must be greater than fastperiod")
        return v

    class Config:
        schema_extra = {
            "examples": {
                "RSI": {
                    "summary": "RSI Example",
                    "value": {
                        "real": [100.0, 101.0, 102.0, 101.5, 103.0],
                        "timeperiod": 14
                    }
                },
                "MACD": {
                    "summary": "MACD Example",
                    "value": {
                        "real": [100.0, 101.0, 102.0, 101.5, 103.0],
                        "fastperiod": 12,
                        "slowperiod": 26,
                        "signalperiod": 9
                    }
                }
            }
        }

class VolumeTalibRequest(TalibRequest):
    """Request model for volume indicators."""
    timeperiod: Optional[int] = Field(
        None,
        description="Number of periods",
        ge=1,
        le=100000,
        example=14
    )
    volume: Optional[List[float]] = Field(
        None,
        description="Volume data",
        min_items=2,
        max_items=100000,
        example=[1000.0, 1500.0, 1400.0, 1800.0, 2000.0]
    )

    @validator('volume')
    def validate_volume(cls, v):
        if v is not None:
            if any(not isinstance(x, (int, float)) or x < 0 or np.isnan(x) or np.isinf(x) for x in v):
                raise ValueError("Volume data must contain only valid non-negative numbers")
        return v

    class Config:
        schema_extra = {
            "example": {
                "real": [100.0, 101.0, 102.0, 101.5, 103.0],
                "volume": [1000.0, 1500.0, 1400.0, 1800.0, 2000.0]
            }
        }

class VolatilityTalibRequest(TalibRequest):
    """Request model for volatility indicators."""
    timeperiod: Optional[int] = Field(
        None,
        description="Number of periods",
        ge=1,
        le=100000,
        example=14
    )
    high: Optional[List[float]] = Field(
        None,
        description="High prices",
        min_items=2,
        max_items=100000
    )
    low: Optional[List[float]] = Field(
        None,
        description="Low prices",
        min_items=2,
        max_items=100000
    )
    close: Optional[List[float]] = Field(
        None,
        description="Close prices",
        min_items=2,
        max_items=100000
    )

    @validator('high')
    def validate_high_low(cls, v, values):
        if v is not None and 'low' in values and values['low'] is not None:
            if len(v) != len(values['low']):
                raise ValueError("high and low arrays must have the same length")
            if any(h < l for h, l in zip(v, values['low'])):
                raise ValueError("high values must be greater than or equal to low values")
        return v

    class Config:
        schema_extra = {
            "example": {
                "high": [102.0, 103.0, 104.0, 103.5, 105.0],
                "low": [99.0, 100.0, 101.0, 100.5, 102.0],
                "close": [100.0, 101.0, 102.0, 101.5, 103.0],
                "timeperiod": 14
            }
        }

class PriceTalibRequest(TalibRequest):
    """Request model for Price Transform functions."""
    high: Optional[List[float]] = Field(None, description="High price series")
    low: Optional[List[float]] = Field(None, description="Low price series")
    close: Optional[List[float]] = Field(None, description="Close price series")
    open: Optional[List[float]] = Field(None, description="Open price series")

class PatternTalibRequest(TalibRequest):
    """Request model for Pattern Recognition functions."""
    open: Optional[List[float]] = Field(None, description="Open price series")
    high: Optional[List[float]] = Field(None, description="High price series")
    low: Optional[List[float]] = Field(None, description="Low price series")
    close: Optional[List[float]] = Field(None, description="Close price series")
    penetration: Optional[float] = Field(None, description="Penetration")

class StatisticTalibRequest(TalibRequest):
    """Request model for Statistic Functions."""
    real0: Optional[List[float]] = Field(None, description="First data series")
    real1: Optional[List[float]] = Field(None, description="Second data series")
    timeperiod: Optional[int] = Field(None, description="Number of periods")
    nbdev: Optional[float] = Field(None, description="Number of deviations")

class MathOperatorTalibRequest(TalibRequest):
    """Request model for Math Operator functions."""
    real0: Optional[List[float]] = Field(None, description="First data series")
    real1: Optional[List[float]] = Field(None, description="Second data series")
    timeperiod: Optional[int] = Field(None, description="Number of periods")
    