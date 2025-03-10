volume_functions = {
    # Volume Indicator Functions
    # AD - Chaikin A/D Line
    "AD": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "volume": ""
        },
        "outputs": ["real"]
    },
    # ADOSC - Chaikin A/D Oscillator
    "ADOSC": {
        "inputs": {
            "high": "",
            "low": "",
            "close": "",
            "volume": "",
            "fastperiod": 3,
            "slowperiod": 10
        },
        "outputs": ["real"]
    },
    # OBV - On Balance Volume
    "OBV": {
        "inputs": {
            "close": "",
            "volume": ""
        },
        "outputs": ["real"]
    }
}