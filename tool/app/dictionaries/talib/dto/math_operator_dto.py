from typing import List

from app.dictionaries.talib.dto.basic_dto import TalibDto, DefaultDto, MathOperatorDefaultDto

class Add_dto(MathOperatorDefaultDto):
    """DTO for ADD function."""
    pass

class Div_dto(MathOperatorDefaultDto):
    """DTO for DIV function."""
    pass

class Max_dto(DefaultDto):
    """DTO for MAX function."""
    timeperiod: int = 30

class Maxindex_dto(DefaultDto):
    """DTO for MAXINDEX function."""
    timeperiod: int = 30

class Min_dto(DefaultDto):
    """DTO for MIN function."""
    timeperiod: int = 30

class Minindex_dto(DefaultDto):
    """DTO for MININDEX function."""
    timeperiod: int = 30

class Minmax_dto(DefaultDto):
    """DTO for MINMAX function."""
    timeperiod: int = 30

class Minmaxindex_dto(DefaultDto):
    """DTO for MINMAXINDEX function."""
    timeperiod: int = 30

class Mult_dto(MathOperatorDefaultDto):
    """DTO for MULT function."""
    pass

class Sub_dto(MathOperatorDefaultDto):
    """DTO for SUB function."""
    pass

class Sum_dto(DefaultDto):
    """DTO for SUM function."""
    timeperiod: int = 30 