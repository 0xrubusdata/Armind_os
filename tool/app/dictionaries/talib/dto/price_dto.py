from typing import List

from app.dictionaries.talib.dto.basic_dto import TalibDto
from app.dictionaries.talib.dto.others_dto import AvgpriceDto, MedpriceDto, TyppriceDto, WclpriceDto

class Avgprice_dto(AvgpriceDto):
    """DTO for AVGPRICE function."""
    pass

class Medprice_dto(MedpriceDto):
    """DTO for MEDPRICE function."""
    pass

class Typprice_dto(TyppriceDto):
    """DTO for TYPPRICE function."""
    pass

class Wclprice_dto(WclpriceDto):
    """DTO for WCLPRICE function."""
    pass 