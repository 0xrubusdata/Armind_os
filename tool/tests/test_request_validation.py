import pytest
from pydantic import ValidationError
from app.models.request.talib_request import (
    TalibRequest,
    MomentumTalibRequest,
    VolatilityTalibRequest,
    VolumeTalibRequest
)

def test_base_request_validation():
    """Test base request validation."""
    # Test valid request
    valid_data = {"real": [1.0, 2.0, 3.0]}
    request = TalibRequest(**valid_data)
    assert request.real == valid_data["real"]
    
    # Test empty data
    with pytest.raises(ValidationError) as exc_info:
        TalibRequest(**{"real": []})
    assert "Price data cannot be empty" in str(exc_info.value)
    
    # Test invalid numbers
    with pytest.raises(ValidationError) as exc_info:
        TalibRequest(**{"real": [1.0, float('nan'), 3.0]})
    assert "Price data must contain only valid numbers" in str(exc_info.value)

def test_momentum_request_validation():
    """Test momentum request validation."""
    # Test valid request
    valid_data = {
        "real": [1.0, 2.0, 3.0],
        "timeperiod": 2,
        "fastperiod": 12,
        "slowperiod": 26,
        "signalperiod": 9
    }
    request = MomentumTalibRequest(**valid_data)
    assert request.real == valid_data["real"]
    assert request.timeperiod == valid_data["timeperiod"]
    
    # Test invalid timeperiod
    with pytest.raises(ValidationError) as exc_info:
        MomentumTalibRequest(**{
            "real": [1.0, 2.0, 3.0],
            "timeperiod": 0
        })
    assert "greater than or equal to 1" in str(exc_info.value)
    
    # Test invalid period relationships
    with pytest.raises(ValidationError) as exc_info:
        MomentumTalibRequest(**{
            "real": [1.0, 2.0, 3.0],
            "fastperiod": 26,
            "slowperiod": 12
        })
    assert "slowperiod must be greater than fastperiod" in str(exc_info.value)

def test_volatility_request_validation(sample_price_data):
    """Test volatility request validation."""
    # Test valid request
    valid_data = {
        "high": sample_price_data["high"],
        "low": sample_price_data["low"],
        "close": sample_price_data["close"],
        "timeperiod": 14
    }
    request = VolatilityTalibRequest(**valid_data)
    assert len(request.high) == len(request.low)
    
    # Test mismatched array lengths
    invalid_data = valid_data.copy()
    invalid_data["low"] = invalid_data["low"][:-1]
    with pytest.raises(ValidationError) as exc_info:
        VolatilityTalibRequest(**invalid_data)
    assert "high and low arrays must have the same length" in str(exc_info.value)
    
    # Test high < low validation
    invalid_data = valid_data.copy()
    invalid_data["high"] = [x - 1 for x in invalid_data["low"]]
    with pytest.raises(ValidationError) as exc_info:
        VolatilityTalibRequest(**invalid_data)
    assert "high values must be greater than or equal to low values" in str(exc_info.value)

def test_volume_request_validation(sample_price_data):
    """Test volume request validation."""
    # Test valid request
    valid_data = {
        "real": sample_price_data["close"],
        "volume": sample_price_data["volume"]
    }
    request = VolumeTalibRequest(**valid_data)
    assert len(request.real) == len(request.volume)
    
    # Test negative volume
    invalid_data = valid_data.copy()
    invalid_data["volume"] = [-1 * v for v in invalid_data["volume"]]
    with pytest.raises(ValidationError) as exc_info:
        VolumeTalibRequest(**invalid_data)
    assert "Volume data must contain only valid non-negative numbers" in str(exc_info.value) 