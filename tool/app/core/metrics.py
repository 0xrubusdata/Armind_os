from prometheus_client import Counter, Histogram, Gauge
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
import time
from typing import Callable

# Create custom metrics
REQUESTS_PROCESSING_TIME = Histogram(
    "talib_request_processing_seconds",
    "Time spent processing request",
    ["endpoint", "method"]
)

FUNCTION_CALLS = Counter(
    "talib_function_calls_total",
    "Number of TA-Lib function calls",
    ["function_name", "category"]
)

ACTIVE_REQUESTS = Gauge(
    "active_requests",
    "Number of currently active requests"
)

ERROR_COUNTER = Counter(
    "errors_total",
    "Total number of errors",
    ["error_type"]
)

# Cache metrics
CACHE_HITS = Counter(
    "cache_hits_total",
    "Total number of cache hits",
    ["function"]
)

CACHE_MISSES = Counter(
    "cache_misses_total",
    "Total number of cache misses",
    ["function"]
)

CACHE_SIZE = Gauge(
    "cache_size",
    "Current number of items in cache"
)

# Performance metrics
CALCULATION_TIME = Histogram(
    "calculation_duration_seconds",
    "Time spent calculating indicators",
    ["function"],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)
)

def bytes_to_mb(bytes_amount: float) -> float:
    """Convert bytes to megabytes."""
    return bytes_amount / 1024 / 1024

def create_memory_metrics(info: Info) -> None:
    """Create memory usage metrics."""
    import psutil
    process = psutil.Process()
    memory_info = process.memory_info()
    
    info.metric(
        "process_memory_rss_mb",
        "Memory usage (RSS) in megabytes",
        bytes_to_mb(memory_info.rss)
    )
    info.metric(
        "process_memory_vms_mb",
        "Memory usage (VMS) in megabytes",
        bytes_to_mb(memory_info.vms)
    )

def create_cpu_metrics(info: Info) -> None:
    """Create CPU usage metrics."""
    import psutil
    process = psutil.Process()
    info.metric(
        "process_cpu_usage_percent",
        "CPU usage percentage",
        process.cpu_percent()
    )

def instrument_app() -> Instrumentator:
    """Configure and return a Prometheus instrumentator."""
    
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/metrics"],
        env_var_name="ENABLE_METRICS",
        inprogress_name="http_requests_inprogress",
        inprogress_labels=True,
    )

    # Add default metrics
    instrumentator.add(
        metrics.request_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_namespace="http",
            metric_subsystem="",
        )
    )
    instrumentator.add(
        metrics.response_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_namespace="http",
            metric_subsystem="",
        )
    )
    instrumentator.add(
        metrics.latency(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_namespace="http",
            metric_subsystem="",
        )
    )
    
    return instrumentator 