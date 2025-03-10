from typing import List, Optional

from app.dictionaries.talib.dto.basic_dto import TalibDto

class MomentumDefaultDto(TalibDto):
    real: List[float]
    timeperiod: int = 10

class MomentumTimeperiodDto(TalibDto):
    high: List[float]
    low: List[float]
    timeperiod: int = 14

class MomentumCloseDto(TalibDto):
    high: List[float]
    low: List[float]
    close: List[float]
    timeperiod: int = 14

class ApoDto(TalibDto):
    real: List[float]
    fastperiod: int = 12
    slowperiod: int = 26
    matype: int = 0

class BopDto(TalibDto):
    open: List[float]
    high: List[float]
    low: List[float]
    close: List[float]

class CmoDto(TalibDto):
    real: List[float]
    timeperiod: int = 14

class MacdDto(TalibDto):
    real: List[float]
    fastperiod: int = 12
    slowperiod: int = 26
    signalperiod: int = 9

class MacdextDto(TalibDto):
    real: List[float]
    fastperiod: int = 12
    fastmatype: int = 0
    slowperiod: int = 26
    slowmatype: int = 0
    signalperiod: int = 9
    signalmatype: int = 0

class MacdfixDto(TalibDto):
    real: List[float]
    signalperiod: int = 9

class MfiDto(TalibDto):
    high: List[float]
    low: List[float]
    close: List[float]
    volume: List[float]
    timeperiod: int = 14

class PpoDto(TalibDto):
    real: List[float]
    fastperiod: int = 12
    slowperiod: int = 26
    matype: int = 0

class RsiDto(TalibDto):
    real: List[float]
    timeperiod: int = 14

class StochDto(TalibDto):
    high: List[float]
    low: List[float]
    close: List[float]
    fastk_period: int = 5
    slowk_period: int = 3
    slowk_matype: int = 0
    slowd_period: int = 3
    slowd_matype: int = 0

class StochfDto(TalibDto):
    high: List[float]
    low: List[float]
    close: List[float]
    fastk_period: int = 5
    fastd_period: int = 3
    fastd_matype: int = 0

class StochrsiDto(TalibDto):
    real: List[float]
    timeperiod: int = 14
    fastk_period: int = 5
    fastd_period: int = 3
    fastd_matype: int = 0
