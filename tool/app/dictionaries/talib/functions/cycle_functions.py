cycle_functions = {
    # Cycle Indicator Functions
    # HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period
    "HT_DCPERIOD": {
        "inputs": {
            "real": ""
        },
        "outputs": ["real"]
    },
    # HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase
    "HT_DCPHASE": {
        "inputs": {
            "real": ""
        },
        "outputs": ["real"]
    },
    # HT_PHASOR - Hilbert Transform - Phasor Components
    "HT_PHASOR": {
        "inputs": {
            "real": ""
        },
        "outputs": ["inphase", "quadrature"]
    },
    # HT_SINE - Hilbert Transform - SineWave
    "HT_SINE": {
        "inputs": {
            "real": ""
        },
        "outputs": ["sine", "leadsine"]
    },
    # HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode
    "HT_TRENDMODE": {
        "inputs": {
            "real": ""
        },
        "outputs": ["integer"]
    }
}