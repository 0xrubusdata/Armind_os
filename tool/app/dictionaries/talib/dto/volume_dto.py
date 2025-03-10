from typing import List

from app.dictionaries.talib.dto.basic_dto import TalibDto, ObvDto, AdDto, AdoscDto

# Volume DTOs are already defined in basic_dto.py:
# ObvDto, AdDto, AdoscDto

class Ad_dto(AdDto):
    """DTO for AD function."""
    pass

class Adosc_dto(AdoscDto):
    """DTO for ADOSC function."""
    pass

class Obv_dto(ObvDto):
    """DTO for OBV function."""
    pass 