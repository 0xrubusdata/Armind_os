from typing import List

from app.dictionaries.talib.dto.basic_dto import TalibDto
from app.dictionaries.talib.dto.others_dto import PatternDefaultDto, PatternPenetrationDto

# Pattern recognition functions use the same DTOs
# Create specific DTOs for each function for better type hinting

# Pattern functions without penetration parameter
class Cdl2crows_dto(PatternDefaultDto):
    """DTO for CDL2CROWS function."""
    pass

class Cdl3blackcrows_dto(PatternDefaultDto):
    """DTO for CDL3BLACKCROWS function."""
    pass

class Cdl3inside_dto(PatternDefaultDto):
    """DTO for CDL3INSIDE function."""
    pass

class Cdl3linestrike_dto(PatternDefaultDto):
    """DTO for CDL3LINESTRIKE function."""
    pass

class Cdl3outside_dto(PatternDefaultDto):
    """DTO for CDL3OUTSIDE function."""
    pass

class Cdl3starsinsouth_dto(PatternDefaultDto):
    """DTO for CDL3STARSINSOUTH function."""
    pass

class Cdl3whitesoldiers_dto(PatternDefaultDto):
    """DTO for CDL3WHITESOLDIERS function."""
    pass

class Cdlabandonedbaby_dto(PatternPenetrationDto):
    """DTO for CDLABANDONEDBABY function."""
    pass

class Cdladvanceblock_dto(PatternDefaultDto):
    """DTO for CDLADVANCEBLOCK function."""
    pass

class Cdlbelthold_dto(PatternDefaultDto):
    """DTO for CDLBELTHOLD function."""
    pass

class Cdlbreakaway_dto(PatternDefaultDto):
    """DTO for CDLBREAKAWAY function."""
    pass

class Cdlclosingmarubozu_dto(PatternDefaultDto):
    """DTO for CDLCLOSINGMARUBOZU function."""
    pass

class Cdlconcealbabyswall_dto(PatternDefaultDto):
    """DTO for CDLCONCEALBABYSWALL function."""
    pass

class Cdlcounterattack_dto(PatternDefaultDto):
    """DTO for CDLCOUNTERATTACK function."""
    pass

class Cdldarkcloudcover_dto(PatternPenetrationDto):
    """DTO for CDLDARKCLOUDCOVER function."""
    pass

class Cdldoji_dto(PatternDefaultDto):
    """DTO for CDLDOJI function."""
    pass

class Cdldojistar_dto(PatternDefaultDto):
    """DTO for CDLDOJISTAR function."""
    pass

class Cdldragonflydoji_dto(PatternDefaultDto):
    """DTO for CDLDRAGONFLYDOJI function."""
    pass

class Cdlengulfing_dto(PatternDefaultDto):
    """DTO for CDLENGULFING function."""
    pass

class Cdleveningdojistar_dto(PatternPenetrationDto):
    """DTO for CDLEVENINGDOJISTAR function."""
    pass

class Cdleveningstar_dto(PatternPenetrationDto):
    """DTO for CDLEVENINGSTAR function."""
    pass

class Cdlgapsidesidewhite_dto(PatternDefaultDto):
    """DTO for CDLGAPSIDESIDEWHITE function."""
    pass

class Cdlgravestonedoji_dto(PatternDefaultDto):
    """DTO for CDLGRAVESTONEDOJI function."""
    pass

class Cdlhammer_dto(PatternDefaultDto):
    """DTO for CDLHAMMER function."""
    pass

class Cdlhangingman_dto(PatternDefaultDto):
    """DTO for CDLHANGINGMAN function."""
    pass

class Cdlharami_dto(PatternDefaultDto):
    """DTO for CDLHARAMI function."""
    pass

class Cdlharamicross_dto(PatternDefaultDto):
    """DTO for CDLHARAMICROSS function."""
    pass

class Cdlhighwave_dto(PatternDefaultDto):
    """DTO for CDLHIGHWAVE function."""
    pass

class Cdlhikkake_dto(PatternDefaultDto):
    """DTO for CDLHIKKAKE function."""
    pass

class Cdlhikkakemod_dto(PatternDefaultDto):
    """DTO for CDLHIKKAKEMOD function."""
    pass

class Cdlhomingpigeon_dto(PatternDefaultDto):
    """DTO for CDLHOMINGPIGEON function."""
    pass

class Cdlidentical3crows_dto(PatternDefaultDto):
    """DTO for CDLIDENTICAL3CROWS function."""
    pass

class Cdlinneck_dto(PatternDefaultDto):
    """DTO for CDLINNECK function."""
    pass

class Cdlinvertedhammer_dto(PatternDefaultDto):
    """DTO for CDLINVERTEDHAMMER function."""
    pass

class Cdlkicking_dto(PatternDefaultDto):
    """DTO for CDLKICKING function."""
    pass

class Cdlkickingbylength_dto(PatternDefaultDto):
    """DTO for CDLKICKINGBYLENGTH function."""
    pass

class Cdlladderbottom_dto(PatternDefaultDto):
    """DTO for CDLLADDERBOTTOM function."""
    pass

class Cdllongleggeddoji_dto(PatternDefaultDto):
    """DTO for CDLLONGLEGGEDDOJI function."""
    pass

class Cdllongline_dto(PatternDefaultDto):
    """DTO for CDLLONGLINE function."""
    pass

class Cdlmarubozu_dto(PatternDefaultDto):
    """DTO for CDLMARUBOZU function."""
    pass

class Cdlmatchinglow_dto(PatternDefaultDto):
    """DTO for CDLMATCHINGLOW function."""
    pass

class Cdlmathold_dto(PatternPenetrationDto):
    """DTO for CDLMATHOLD function."""
    pass

class Cdlmorningdojistar_dto(PatternPenetrationDto):
    """DTO for CDLMORNINGDOJISTAR function."""
    pass

class Cdlmorningstar_dto(PatternPenetrationDto):
    """DTO for CDLMORNINGSTAR function."""
    pass

class Cdlonneck_dto(PatternDefaultDto):
    """DTO for CDLONNECK function."""
    pass

class Cdlpiercing_dto(PatternDefaultDto):
    """DTO for CDLPIERCING function."""
    pass

class Cdlrickshawman_dto(PatternDefaultDto):
    """DTO for CDLRICKSHAWMAN function."""
    pass

class Cdlrisefall3methods_dto(PatternDefaultDto):
    """DTO for CDLRISEFALL3METHODS function."""
    pass

class Cdlseparatinglines_dto(PatternDefaultDto):
    """DTO for CDLSEPARATINGLINES function."""
    pass

class Cdlshootingstar_dto(PatternDefaultDto):
    """DTO for CDLSHOOTINGSTAR function."""
    pass

class Cdlshortline_dto(PatternDefaultDto):
    """DTO for CDLSHORTLINE function."""
    pass

class Cdlspinningtop_dto(PatternDefaultDto):
    """DTO for CDLSPINNINGTOP function."""
    pass

class Cdlstalledpattern_dto(PatternDefaultDto):
    """DTO for CDLSTALLEDPATTERN function."""
    pass

class Cdlsticksandwich_dto(PatternDefaultDto):
    """DTO for CDLSTICKSANDWICH function."""
    pass

class Cdltakuri_dto(PatternDefaultDto):
    """DTO for CDLTAKURI function."""
    pass

class Cdltasukigap_dto(PatternDefaultDto):
    """DTO for CDLTASUKIGAP function."""
    pass

class Cdlthrusting_dto(PatternDefaultDto):
    """DTO for CDLTHRUSTING function."""
    pass

class Cdltristar_dto(PatternDefaultDto):
    """DTO for CDLTRISTAR function."""
    pass

class Cdlunique3river_dto(PatternDefaultDto):
    """DTO for CDLUNIQUE3RIVER function."""
    pass

class Cdlupsidegap2crows_dto(PatternDefaultDto):
    """DTO for CDLUPSIDEGAP2CROWS function."""
    pass

class Cdlxsidegap3methods_dto(PatternDefaultDto):
    """DTO for CDLXSIDEGAP3METHODS function."""
    pass 