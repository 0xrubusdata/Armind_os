from typing import List

from app.dictionaries.talib.dto.basic_dto import TalibDto, TrangeDto, AtrDto, NatrDto

# Some volatility DTOs are already defined in basic_dto.py:
# TrangeDto, AtrDto, NatrDto

class Atr_dto(AtrDto):
    """DTO for ATR function."""
    pass

class Natr_dto(NatrDto):
    """DTO for NATR function."""
    pass

class Trange_dto(TrangeDto):
    """DTO for TRANGE function."""
    pass 