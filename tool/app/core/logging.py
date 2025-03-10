import logging
import sys
from pythonjsonlogger import jsonlogger
from datetime import datetime
from app.core.config import settings

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno

def setup_logging():
    """Configure logging with JSON formatting and appropriate handlers."""
    # Create logger
    logger = logging.getLogger("talib_api")
    logger.setLevel(settings.LOG_LEVEL)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL)
    
    # Create JSON formatter
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(module)s %(function)s %(line)s %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger

# Create logger instance
logger = setup_logging()

def log_request_details(request, processing_time=None, error=None):
    """Log detailed request information."""
    log_data = {
        "client_ip": request.client.host,
        "method": request.method,
        "url": str(request.url),
        "path_params": request.path_params,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "processing_time": f"{processing_time:.4f}s" if processing_time else None,
        "error": str(error) if error else None
    }
    
    if error:
        logger.error("Request failed", extra=log_data)
    else:
        logger.info("Request processed", extra=log_data)

def log_function_call(function_name, category, params, duration, error=None):
    """Log TA-Lib function call details."""
    log_data = {
        "function": function_name,
        "category": category,
        "parameters": params,
        "duration": f"{duration:.4f}s",
        "error": str(error) if error else None
    }
    
    if error:
        logger.error("Function call failed", extra=log_data)
    else:
        logger.info("Function call completed", extra=log_data) 