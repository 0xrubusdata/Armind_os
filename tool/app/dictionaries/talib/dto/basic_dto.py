from pydantic import BaseModel
from typing import List

class TalibDto(BaseModel):
    #Attributs et methodes communs ici
    pass

class DefaultDto(TalibDto):
    real: List[float]

class DefaultTimeperiodDto(TalibDto):
    real: List[float]
    timeperiod: int = 30    

class MathOperatorDefaultDto(TalibDto):
    real0: List[float]
    real1: List[float]    

class TrangeDto(TalibDto):
    high: List[float]
    low: List[float]
    close: List[float]
    
class AtrDto(TrangeDto):
    timeperiod: int = 14

class NatrDto(TrangeDto):
    timeperiod: int = 14    
    
class ObvDto(TalibDto):
    close: List[float]
    volume: List[float]
    
class AdDto(ObvDto):
    high: List[float]
    low: List[float]
    
class AdoscDto(AdDto):
    fastperiod: int = 3
    slowperiod: int = 10    