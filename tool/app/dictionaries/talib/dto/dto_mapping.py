# Import all DTOs
from app.dictionaries.talib.dto.momentum_dto import (
    MomentumDefaultDto, MomentumTimeperiodDto, MomentumCloseDto,
    ApoDto, BopDto, CmoDto, MacdDto, MacdextDto, MacdfixDto,
    MfiDto, PpoDto, RsiDto, StochDto, StochfDto, StochrsiDto
)
from app.dictionaries.talib.dto.overlap_dto import (
    BbandsDto, HtTrendlineDto, MaDto, MamaDto, MavpDto,
    MidpointDto, MidpriceDto, SarDto, SarextDto, T3Dto
)
from app.dictionaries.talib.dto.volume_dto import (
    Ad_dto, Adosc_dto, Obv_dto
)
from app.dictionaries.talib.dto.volatility_dto import (
    Atr_dto, Natr_dto, Trange_dto
)
from app.dictionaries.talib.dto.price_dto import (
    Avgprice_dto, Medprice_dto, Typprice_dto, Wclprice_dto
)
from app.dictionaries.talib.dto.pattern_dto import (
    Cdl2crows_dto, Cdl3blackcrows_dto, Cdl3inside_dto, Cdl3linestrike_dto,
    Cdl3outside_dto, Cdl3starsinsouth_dto, Cdl3whitesoldiers_dto,
    Cdlabandonedbaby_dto, Cdladvanceblock_dto, Cdlbelthold_dto,
    Cdlbreakaway_dto, Cdlclosingmarubozu_dto, Cdlconcealbabyswall_dto,
    Cdlcounterattack_dto, Cdldarkcloudcover_dto, Cdldoji_dto,
    Cdldojistar_dto, Cdldragonflydoji_dto, Cdlengulfing_dto,
    Cdleveningdojistar_dto, Cdleveningstar_dto, Cdlgapsidesidewhite_dto,
    Cdlgravestonedoji_dto, Cdlhammer_dto, Cdlhangingman_dto,
    Cdlharami_dto, Cdlharamicross_dto, Cdlhighwave_dto,
    Cdlhikkake_dto, Cdlhikkakemod_dto, Cdlhomingpigeon_dto,
    Cdlidentical3crows_dto, Cdlinneck_dto, Cdlinvertedhammer_dto,
    Cdlkicking_dto, Cdlkickingbylength_dto, Cdlladderbottom_dto,
    Cdllongleggeddoji_dto, Cdllongline_dto, Cdlmarubozu_dto,
    Cdlmatchinglow_dto, Cdlmathold_dto, Cdlmorningdojistar_dto,
    Cdlmorningstar_dto, Cdlonneck_dto, Cdlpiercing_dto,
    Cdlrickshawman_dto, Cdlrisefall3methods_dto, Cdlseparatinglines_dto,
    Cdlshootingstar_dto, Cdlshortline_dto, Cdlspinningtop_dto,
    Cdlstalledpattern_dto, Cdlsticksandwich_dto, Cdltakuri_dto,
    Cdltasukigap_dto, Cdlthrusting_dto, Cdltristar_dto,
    Cdlunique3river_dto, Cdlupsidegap2crows_dto, Cdlxsidegap3methods_dto
)
from app.dictionaries.talib.dto.statistic_dto import (
    Beta_dto, Correl_dto, Linearreg_dto, Linearreg_angle_dto,
    Linearreg_intercept_dto, Linearreg_slope_dto, Stddev_dto,
    Tsf_dto, Var_dto
)
from app.dictionaries.talib.dto.math_transform_dto import (
    Acos_dto, Asin_dto, Atan_dto, Ceil_dto, Cos_dto, Cosh_dto,
    Exp_dto, Floor_dto, Ln_dto, Log10_dto, Sin_dto, Sinh_dto,
    Sqrt_dto, Tan_dto, Tanh_dto
)
from app.dictionaries.talib.dto.math_operator_dto import (
    Add_dto, Div_dto, Max_dto, Maxindex_dto, Min_dto, Minindex_dto,
    Minmax_dto, Minmaxindex_dto, Mult_dto, Sub_dto, Sum_dto
)
from app.dictionaries.talib.dto.cycle_dto import (
    Ht_dcperiod_dto, Ht_dcphase_dto, Ht_phasor_dto, Ht_sine_dto,
    Ht_trendmode_dto
)

# Create dictionaries mapping function names to their respective DTOs
momentum_dto_dict = {
    "APO": ApoDto,
    "BOP": BopDto,
    "CMO": CmoDto,
    "MACD": MacdDto,
    "MACDEXT": MacdextDto,
    "MACDFIX": MacdfixDto,
    "MFI": MfiDto,
    "MOM": MomentumDefaultDto,
    "PPO": PpoDto,
    "ROC": MomentumDefaultDto,
    "ROCP": MomentumDefaultDto,
    "ROCR": MomentumDefaultDto,
    "ROCR100": MomentumDefaultDto,
    "RSI": RsiDto,
    "STOCH": StochDto,
    "STOCHF": StochfDto,
    "STOCHRSI": StochrsiDto,
    "TRIX": MomentumDefaultDto,
    "ULTOSC": MomentumCloseDto,
    "WILLR": MomentumTimeperiodDto
}

overlap_dto_dict = {
    "BBANDS": BbandsDto,
    "DEMA": MaDto,
    "EMA": MaDto,
    "HT_TRENDLINE": HtTrendlineDto,
    "KAMA": MaDto,
    "MA": MaDto,
    "MAMA": MamaDto,
    "MAVP": MavpDto,
    "MIDPOINT": MidpointDto,
    "MIDPRICE": MidpriceDto,
    "SAR": SarDto,
    "SAREXT": SarextDto,
    "SMA": MaDto,
    "T3": T3Dto,
    "TEMA": MaDto,
    "TRIMA": MaDto,
    "WMA": MaDto
}

volume_dto_dict = {
    "AD": Ad_dto,
    "ADOSC": Adosc_dto,
    "OBV": Obv_dto
}

volatility_dto_dict = {
    "ATR": Atr_dto,
    "NATR": Natr_dto,
    "TRANGE": Trange_dto
}

price_dto_dict = {
    "AVGPRICE": Avgprice_dto,
    "MEDPRICE": Medprice_dto,
    "TYPPRICE": Typprice_dto,
    "WCLPRICE": Wclprice_dto
}

pattern_dto_dict = {
    "CDL2CROWS": Cdl2crows_dto,
    "CDL3BLACKCROWS": Cdl3blackcrows_dto,
    "CDL3INSIDE": Cdl3inside_dto,
    "CDL3LINESTRIKE": Cdl3linestrike_dto,
    "CDL3OUTSIDE": Cdl3outside_dto,
    "CDL3STARSINSOUTH": Cdl3starsinsouth_dto,
    "CDL3WHITESOLDIERS": Cdl3whitesoldiers_dto,
    "CDLABANDONEDBABY": Cdlabandonedbaby_dto,
    "CDLADVANCEBLOCK": Cdladvanceblock_dto,
    "CDLBELTHOLD": Cdlbelthold_dto,
    "CDLBREAKAWAY": Cdlbreakaway_dto,
    "CDLCLOSINGMARUBOZU": Cdlclosingmarubozu_dto,
    "CDLCONCEALBABYSWALL": Cdlconcealbabyswall_dto,
    "CDLCOUNTERATTACK": Cdlcounterattack_dto,
    "CDLDARKCLOUDCOVER": Cdldarkcloudcover_dto,
    "CDLDOJI": Cdldoji_dto,
    "CDLDOJISTAR": Cdldojistar_dto,
    "CDLDRAGONFLYDOJI": Cdldragonflydoji_dto,
    "CDLENGULFING": Cdlengulfing_dto,
    "CDLEVENINGDOJISTAR": Cdleveningdojistar_dto,
    "CDLEVENINGSTAR": Cdleveningstar_dto,
    "CDLGAPSIDESIDEWHITE": Cdlgapsidesidewhite_dto,
    "CDLGRAVESTONEDOJI": Cdlgravestonedoji_dto,
    "CDLHAMMER": Cdlhammer_dto,
    "CDLHANGINGMAN": Cdlhangingman_dto,
    "CDLHARAMI": Cdlharami_dto,
    "CDLHARAMICROSS": Cdlharamicross_dto,
    "CDLHIGHWAVE": Cdlhighwave_dto,
    "CDLHIKKAKE": Cdlhikkake_dto,
    "CDLHIKKAKEMOD": Cdlhikkakemod_dto,
    "CDLHOMINGPIGEON": Cdlhomingpigeon_dto,
    "CDLIDENTICAL3CROWS": Cdlidentical3crows_dto,
    "CDLINNECK": Cdlinneck_dto,
    "CDLINVERTEDHAMMER": Cdlinvertedhammer_dto,
    "CDLKICKING": Cdlkicking_dto,
    "CDLKICKINGBYLENGTH": Cdlkickingbylength_dto,
    "CDLLADDERBOTTOM": Cdlladderbottom_dto,
    "CDLLONGLEGGEDDOJI": Cdllongleggeddoji_dto,
    "CDLLONGLINE": Cdllongline_dto,
    "CDLMARUBOZU": Cdlmarubozu_dto,
    "CDLMATCHINGLOW": Cdlmatchinglow_dto,
    "CDLMATHOLD": Cdlmathold_dto,
    "CDLMORNINGDOJISTAR": Cdlmorningdojistar_dto,
    "CDLMORNINGSTAR": Cdlmorningstar_dto,
    "CDLONNECK": Cdlonneck_dto,
    "CDLPIERCING": Cdlpiercing_dto,
    "CDLRICKSHAWMAN": Cdlrickshawman_dto,
    "CDLRISEFALL3METHODS": Cdlrisefall3methods_dto,
    "CDLSEPARATINGLINES": Cdlseparatinglines_dto,
    "CDLSHOOTINGSTAR": Cdlshootingstar_dto,
    "CDLSHORTLINE": Cdlshortline_dto,
    "CDLSPINNINGTOP": Cdlspinningtop_dto,
    "CDLSTALLEDPATTERN": Cdlstalledpattern_dto,
    "CDLSTICKSANDWICH": Cdlsticksandwich_dto,
    "CDLTAKURI": Cdltakuri_dto,
    "CDLTASUKIGAP": Cdltasukigap_dto,
    "CDLTHRUSTING": Cdlthrusting_dto,
    "CDLTRISTAR": Cdltristar_dto,
    "CDLUNIQUE3RIVER": Cdlunique3river_dto,
    "CDLUPSIDEGAP2CROWS": Cdlupsidegap2crows_dto,
    "CDLXSIDEGAP3METHODS": Cdlxsidegap3methods_dto
}

statistic_dto_dict = {
    "BETA": Beta_dto,
    "CORREL": Correl_dto,
    "LINEARREG": Linearreg_dto,
    "LINEARREG_ANGLE": Linearreg_angle_dto,
    "LINEARREG_INTERCEPT": Linearreg_intercept_dto,
    "LINEARREG_SLOPE": Linearreg_slope_dto,
    "STDDEV": Stddev_dto,
    "TSF": Tsf_dto,
    "VAR": Var_dto
}

math_transform_dto_dict = {
    "ACOS": Acos_dto,
    "ASIN": Asin_dto,
    "ATAN": Atan_dto,
    "CEIL": Ceil_dto,
    "COS": Cos_dto,
    "COSH": Cosh_dto,
    "EXP": Exp_dto,
    "FLOOR": Floor_dto,
    "LN": Ln_dto,
    "LOG10": Log10_dto,
    "SIN": Sin_dto,
    "SINH": Sinh_dto,
    "SQRT": Sqrt_dto,
    "TAN": Tan_dto,
    "TANH": Tanh_dto
}

math_operator_dto_dict = {
    "ADD": Add_dto,
    "DIV": Div_dto,
    "MAX": Max_dto,
    "MAXINDEX": Maxindex_dto,
    "MIN": Min_dto,
    "MININDEX": Minindex_dto,
    "MINMAX": Minmax_dto,
    "MINMAXINDEX": Minmaxindex_dto,
    "MULT": Mult_dto,
    "SUB": Sub_dto,
    "SUM": Sum_dto
}

cycle_dto_dict = {
    "HT_DCPERIOD": Ht_dcperiod_dto,
    "HT_DCPHASE": Ht_dcphase_dto,
    "HT_PHASOR": Ht_phasor_dto,
    "HT_SINE": Ht_sine_dto,
    "HT_TRENDMODE": Ht_trendmode_dto
}

# Combine all dictionaries into a single mapping
dto_dictionaries = {
    "momentum_functions": momentum_dto_dict,
    "overlap_functions": overlap_dto_dict,
    "volume_functions": volume_dto_dict,
    "volatility_functions": volatility_dto_dict,
    "price_functions": price_dto_dict,
    "pattern_functions": pattern_dto_dict,
    "statistic_functions": statistic_dto_dict,
    "math_transform_functions": math_transform_dto_dict,
    "math_operator_functions": math_operator_dto_dict,
    "cycle_functions": cycle_dto_dict
}
