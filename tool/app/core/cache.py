from functools import wraps
import hashlib
import json
from typing import Any, Dict, Optional
import time
from app.core.config import settings
import asyncio

# Simple in-memory cache
cache: Dict[str, Dict[str, Any]] = {}

def generate_cache_key(func_name: str, *args, **kwargs) -> str:
    """Generate a unique cache key based on function name and arguments."""
    key_parts = [func_name]
    
    # Add positional arguments
    for arg in args:
        if isinstance(arg, (list, dict)):
            # For complex types, use their JSON representation
            key_parts.append(json.dumps(arg, sort_keys=True))
        else:
            key_parts.append(str(arg))
    
    # Add keyword arguments (sorted to ensure consistency)
    for key in sorted(kwargs.keys()):
        value = kwargs[key]
        if isinstance(value, (list, dict)):
            key_parts.append(f"{key}:{json.dumps(value, sort_keys=True)}")
        else:
            key_parts.append(f"{key}:{value}")
    
    # Create a hash of the key parts
    key = hashlib.sha256(":".join(key_parts).encode()).hexdigest()
    return key

def cache_result(ttl: Optional[int] = None):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds. If None, uses settings.CACHE_TTL
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = generate_cache_key(func.__name__, *args, **kwargs)
            
            # Get current time
            current_time = time.time()
            
            # Check if result is in cache and not expired
            if cache_key in cache:
                cached_result = cache[cache_key]
                if current_time < cached_result["expires_at"]:
                    return cached_result["data"]
                else:
                    # Remove expired result
                    del cache[cache_key]
            
            # Calculate result
            result = await func(*args, **kwargs)
            
            # Cache result
            cache[cache_key] = {
                "data": result,
                "expires_at": current_time + (ttl or settings.CACHE_TTL)
            }
            
            return result
        return wrapper
    return decorator

def clear_cache():
    """Clear all cached results."""
    cache.clear()

def cleanup_expired():
    """Remove expired entries from cache."""
    current_time = time.time()
    expired_keys = [
        key for key, value in cache.items()
        if current_time >= value["expires_at"]
    ]
    for key in expired_keys:
        del cache[key]

# Run cleanup periodically (e.g., from a background task)
async def periodic_cleanup():
    """Periodically clean up expired cache entries."""
    while True:
        cleanup_expired()
        await asyncio.sleep(300)  # Clean up every 5 minutes 