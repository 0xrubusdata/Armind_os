momentum_functions = {
    # Momentum Indicator Functions
    # ADX - Average Directional Movement Index
    "ADX": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # ADXR - Average Directional Movement Index Rating
    "ADXR": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # APO - Absolute Price Oscillator
    "APO": {
        "inputs": {
            "real": "",
            "fastperiod": 12,
            "slowperiod": 26,
            "matype": 0
        },
        "outputs": ["real"]
    },
    # AROON - Aroon
    "AROON": {
        "inputs": {
            "high": "",
            "low": "",
            "timeperiod": 14
        },
        "outputs": ["aroondown", "aroonup"]
    },
    # AROONOSC - Aroon Oscillator
    "AROONOSC": {
        "inputs": {
            "high": "",
            "low": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # BOP - Balance Of Power
    "BOP": {
        "inputs": {
            "open": "",
            "high": "",
            "low": "",
            "close": ""
        },
        "outputs": ["real"]
    },
    # CCI - Commodity Channel Index
    "CCI": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # CMO - Chande Momentum Oscillator
    "CMO": {
        "inputs": {
            "real": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # DX - Directional Movement Index
    "DX": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # MACD - Moving Average Convergence/Divergence
    "MACD": {
        "inputs": {
            "real": "",
            "fastperiod": 12,
            "slowperiod": 26,
            "signalperiod": 9
        },
        "outputs": ["macd", "macdsignal", "macdhist"]
    },
    # MACDEXT - MACD with controllable MA type
    "MACDEXT": {
        "inputs": {
            "real": "",
            "fastperiod": 12,
            "fastmatype": 0,
            "slowperiod": 26,
            "slowmatype": 0,
            "signalperiod": 9,
            "signalmatype": 0
        },
        "outputs": ["macd", "macdsignal", "macdhist"]
    },
    # MACDFIX - Moving Average Convergence/Divergence Fix 12/26
    "MACDFIX": {
        "inputs": {
            "real": "",
            "signalperiod": 9
        },
        "outputs": ["macd", "macdsignal", "macdhist"]
    },
    # MFI - Money Flow Index
    "MFI": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "volume": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # MINUS_DI - Minus Directional Indicator
    "MINUS_DI": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # MINUS_DM - Minus Directional Movement
    "MINUS_DM": {
        "inputs": {
            "high": "",
            "low": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # MOM - Momentum
    "MOM": {
        "inputs": {
            "real": "",
            "timeperiod": 10
        },
        "outputs": ["real"]
    },
    # PLUS_DI - Plus Directional Indicator
    "PLUS_DI": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # PLUS_DM - Plus Directional Movement
    "PLUS_DM": {
        "inputs": {
            "high": "",
            "low": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # PPO - Percentage Price Oscillator
    "PPO": {
        "inputs": {
            "real": "",
            "fastperiod": 12,
            "slowperiod": 26,
            "matype": 0
        },
        "outputs": ["real"]
    },
    # ROC - Rate of change : ((price/prevPrice)-1)*100
    "ROC": {
        "inputs": {
            "real": "",
            "timeperiod": 10
        },
        "outputs": ["real"]
    },
    # ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice
    "ROCP": {
        "inputs": {
            "real": "",
            "timeperiod": 10
        },
        "outputs": ["real"]
    },
    # ROCR - Rate of change ratio: (price/prevPrice)
    "ROCR": {
        "inputs": {
            "real": "",
            "timeperiod": 10
        },
        "outputs": ["real"]
    },
    # ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100
    "ROCR100": {
        "inputs": {
            "real": "",
            "timeperiod": 10
        },
        "outputs": ["real"]
    },
    # RSI - Relative Strength Index
    "RSI": {
        "inputs": {
            "real": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # STOCH - Stochastic
    "STOCH": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "fastk_period": 5,
            "slowk_period": 3,
            "slowk_matype": 0,
            "slowd_period": 3,
            "slowd_matype": 0
        },
        "outputs": ["slowk", "slowd"]
    },
    # STOCHF - Stochastic Fast
    "STOCHF": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "fastk_period": 5,
            "fastd_period": 3,
            "fastd_matype": 0
        },
        "outputs": ["fastk", "fastd"]
    },
    # STOCHRSI - Stochastic Relative Strength Index
    "STOCHRSI": {
        "inputs": {
            "real": "",
            "timeperiod": 14,
            "fastk_period": 5,
            "fastd_period": 3,
            "fastd_matype": 0
        },
        "outputs": ["fastk", "fastd"]
    },
    # TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
    "TRIX": {
        "inputs": {
            "real": "",
            "timeperiod": 30
        },
        "outputs": ["real"]
    }
}    