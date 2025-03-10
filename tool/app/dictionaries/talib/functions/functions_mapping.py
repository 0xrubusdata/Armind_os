from app.dictionaries.talib.functions.cycle_functions import ( cycle_functions )
from app.dictionaries.talib.functions.overlap_functions import ( overlap_functions )
from app.dictionaries.talib.functions.momentum_functions import ( momentum_functions )
from app.dictionaries.talib.functions.volume_functions import ( volume_functions )
from app.dictionaries.talib.functions.volatility_functions import ( volatility_functions )
from app.dictionaries.talib.functions.price_functions import ( price_functions )
from app.dictionaries.talib.functions.pattern_functions import ( pattern_functions )
from app.dictionaries.talib.functions.statistic_functions import ( statistic_functions )
from app.dictionaries.talib.functions.math_transform_functions import ( math_transform_functions )
from app.dictionaries.talib.functions.math_operator_functions import ( math_operator_functions )

functions_dictionaries = {
    "cycle_functions": cycle_functions,
    "overlap_functions": overlap_functions,
    "momentum_functions": momentum_functions,
    "volume_functions": volume_functions,
    "volatility_functions": volatility_functions,
    "price_functions": price_functions,
    "pattern_functions": pattern_functions,
    "statistic_functions": statistic_functions,
    "math_transform_functions": math_transform_functions,
    "math_operator_functions": math_operator_functions
}
