overlap_functions = {
    # Overlap Studies Functions
    # BBANDS - Bollinger Bands
    "BBANDS": {
        "inputs": {
            "real": "",
            "timeperiod": 5,
            "nbdevup": 2,
            "nbdevdn": 2,
            "matype": 0
        },
        "outputs": ["upperband", "middleband", "lowerband"]
    },
    # DEMA - Double Exponential Moving Average
    "DEMA": {
        "inputs": {
            "real": "",
            "timeperiod": 30
        },
        "outputs": ["real"]
    },
    # EMA - Exponential Moving Average
    "EMA": {
        "inputs": {
            "real": "",
            "timeperiod": 30
        },
        "outputs": ["real"]
    },
    # HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
    "HT_TRENDLINE": {
        "inputs": {
            "real": ""
        },
        "outputs": ["real"]
    },
    # KAMA - Kaufman Adaptive Moving Average
    "KAMA": {
        "inputs": {
            "real": "",
            "timeperiod": 30
        },
        "outputs": ["real"]
    },
    # MA - Moving average
    "MA": {
        "inputs": {
            "real": "",
            "timeperiod": 30,
            "matype": 0
        },
        "outputs": ["real"]
    },
    # MAMA - MESA Adaptive Moving Average
    "MAMA": {
        "inputs": {
            "real": "",
            "fastlimit": 0,
            "slowlimit": 0
        },
        "outputs": ["mama", "fama"]
    },
    # MAVP - Moving average with variable period
    "MAVP": {
        "inputs": {
            "real": "",
            "periods": "",
            "minperiod": 2,
            "maxperiod": 30,
            "matype": 0
        },
        "outputs": ["real"]
    },
    # MIDPOINT - MidPoint over period
    "MIDPOINT": {
        "inputs": {
            "real": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # MIDPRICE - Midpoint Price over period
    "MIDPRICE": {
        "inputs": {
            "high": "",
            "low": "",
            "timeperiod": 14
        },
        "outputs": ["real"]
    },
    # SAR - Parabolic SAR
    "SAR": {
        "inputs": {
            "high": "",
            "low": "",
            "acceleration": 0,
            "maximum": 0
        },
        "outputs": ["real"]
    },
    # SAREXT - Parabolic SAR - Extended
    "SAREXT": {
        "inputs": {
            "high": "",
            "low": "",
            "startvalue": 0,
            "offsetonreverse": 0,
            "accelerationinitlong": 0,
            "accelerationlong": 0,
            "accelerationmaxlong": 0,
            "accelerationinitshort": 0,
            "accelerationshort": 0,
            "accelerationmaxshort": 0
        },
        "outputs": ["real"]
    },
    # SMA - Simple Moving Average
    "SMA": {
        "inputs": {
            "real": "",
            "timeperiod": 30
        },
        "outputs": ["real"]
    },
    # T3 - Triple Exponential Moving Average (T3)
    "T3": {
        "inputs": {
            "real": "",
            "timeperiod": 5,
            "vfactor": 0
        },
        "outputs": ["real"]
    },
    # TEMA - Triple Exponential Moving Average
    "TEMA": {
        "inputs": {
            "real": "",
            "timeperiod": 30
        },
        "outputs": ["real"]
    },
    # TRIMA - Triangular Moving Average
    "TRIMA": {
        "inputs": {
            "real": "",
            "timeperiod": 30
        },
        "outputs": ["real"]
    },
    # WMA - Weighted Moving Average
    "WMA": {
        "inputs": {
            "real": "",
            "timeperiod": 30
        },
        "outputs": ["real"]
    }
}