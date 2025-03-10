from typing import  List

from app.dictionaries.talib.dto.basic_dto import TalibDto


class BbandsDto(TalibDto):
    real: List[float]
    timeperiod: int = 5
    nbdevup: int = 2
    nbdevdn: int = 2
    matype: int = 0
    
class HtTrendlineDto(TalibDto):
    real: List[float]
    
class MaDto(TalibDto):
    real: List[float]
    timeperiod: int = 30
    matype: int = 0

class MamaDto(TalibDto):
    real: List[float]
    fastlimit: int = 0
    slowlimit: int = 0

class MavpDto(TalibDto):
    real: List[float]
    periods: List[int]
    minperiod: int = 2
    maxperiod: int = 30
    matype: int = 0

class MidpointDto(TalibDto):
    real: List[float]
    timeperiod: int = 14

class MidpriceDto(TalibDto):
    high: List[float]
    low: List[float]
    timeperiod: int = 14

class SarDto(TalibDto):
    high: List[float]
    low: List[float]
    acceleration: int = 0
    maximum: int = 0

class SarextDto(TalibDto):
    high: List[float]
    low: List[float]
    startvalue: int = 0
    offsetonreverse: int = 0
    accelerationinitlong: int = 0
    accelerationlong: int = 0
    accelerationmaxlong: int = 0
    accelerationinitshort: int = 0
    accelerationshort: int = 0
    accelerationmaxshort: int = 0

class T3Dto(TalibDto):
    real: List[float]
    timeperiod: int = 5
    vfactor: int = 0

