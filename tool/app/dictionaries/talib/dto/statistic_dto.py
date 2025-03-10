from typing import List

from app.dictionaries.talib.dto.basic_dto import TalibDto
from app.dictionaries.talib.dto.others_dto import StatisticTimeperiodDto, VarDto, BetaDto, CorrelDto

class Beta_dto(BetaDto):
    """DTO for BETA function."""
    pass

class Correl_dto(CorrelDto):
    """DTO for CORREL function."""
    pass

class Linearreg_dto(StatisticTimeperiodDto):
    """DTO for LINEARREG function."""
    pass

class Linearreg_angle_dto(StatisticTimeperiodDto):
    """DTO for LINEARREG_ANGLE function."""
    pass

class Linearreg_intercept_dto(StatisticTimeperiodDto):
    """DTO for LINEARREG_INTERCEPT function."""
    pass

class Linearreg_slope_dto(StatisticTimeperiodDto):
    """DTO for LINEARREG_SLOPE function."""
    pass

class Stddev_dto(StatisticTimeperiodDto):
    """DTO for STDDEV function."""
    pass

class Tsf_dto(StatisticTimeperiodDto):
    """DTO for TSF function."""
    pass

class Var_dto(VarDto):
    """DTO for VAR function."""
    pass 