from typing import List

from app.dictionaries.talib.dto.basic_dto import TalibDto


class AvgpriceDto(TalibDto):
    open: List[float]
    high: List[float]
    low: List[float]
    close: List[float]

class MedpriceDto(TalibDto):
    high: List[float]
    low: List[float]

class TyppriceDto(TalibDto):
    high: List[float]
    low: List[float]
    close: List[float]

class WclpriceDto(TalibDto):
    high: List[float]
    low: List[float]
    close: List[float]



class StatisticTimeperiodDto(TalibDto):
    real: List[float]
    timeperiod: int = 14

class VarDto(TalibDto):
    real: List[float]
    timeperiod: int = 5
    nbdev: int = 1

class BetaDto(TalibDto):
    real0: List[float]
    real1: List[float]
    timeperiod: int = 5

class CorrelDto(TalibDto):
    real0: List[float]
    real1: List[float]
    timeperiod: int = 30


class PatternDefaultDto(TalibDto):
    open: List[float]
    high: List[float]
    low: List[float]
    close: List[float]

class PatternPenetrationDto(TalibDto):
    open: List[float]
    high: List[float]
    low: List[float]
    close: List[float]
    penetration: float = 0  # Changed to float    