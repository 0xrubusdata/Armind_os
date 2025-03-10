from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
from typing import Dict, List, Optional
import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, requests_per_minute: int = 100, requests_per_hour: int = 1000):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.requests: Dict[str, List[float]] = {}
        self.cleanup_task: Optional[asyncio.Task] = None

    async def cleanup_old_requests(self):
        """Remove requests older than 1 hour."""
        while True:
            current_time = time.time()
            hour_ago = current_time - 3600
            
            # Clean up old requests
            self.requests = {
                ip: [t for t in times if t > hour_ago]
                for ip, times in self.requests.items()
            }
            
            # Remove empty entries
            self.requests = {
                ip: times for ip, times in self.requests.items()
                if times
            }
            
            await asyncio.sleep(60)  # Run cleanup every minute

    def is_rate_limited(self, ip: str) -> tuple[bool, Optional[str]]:
        """
        Check if the request should be rate limited.
        
        Returns:
            tuple[bool, Optional[str]]: (is_limited, error_message)
        """
        current_time = time.time()
        minute_ago = current_time - 60
        hour_ago = current_time - 3600
        
        if ip not in self.requests:
            self.requests[ip] = []
        
        # Get requests in the last minute and hour
        requests_last_minute = len([t for t in self.requests[ip] if t > minute_ago])
        requests_last_hour = len([t for t in self.requests[ip] if t > hour_ago])
        
        if requests_last_minute >= self.requests_per_minute:
            return True, f"Rate limit exceeded: {self.requests_per_minute} requests per minute"
        
        if requests_last_hour >= self.requests_per_hour:
            return True, f"Rate limit exceeded: {self.requests_per_hour} requests per hour"
        
        self.requests[ip].append(current_time)
        return False, None

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        requests_per_minute: int = 100,
        requests_per_hour: int = 1000
    ):
        super().__init__(app)
        self.limiter = RateLimiter(requests_per_minute, requests_per_hour)
        
    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip rate limiting for documentation
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host
        
        # Start cleanup task if not running
        if not self.limiter.cleanup_task:
            self.limiter.cleanup_task = asyncio.create_task(
                self.limiter.cleanup_old_requests()
            )
        
        # Check rate limit
        is_limited, error_message = self.limiter.is_rate_limited(client_ip)
        
        if is_limited:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": error_message,
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "extra": {
                        "retry_after": "60 seconds" if "per minute" in error_message else "1 hour"
                    }
                }
            )
        
        response = await call_next(request)
        
        # Add rate limit headers
        minute_remaining = self.limiter.requests_per_minute - len([
            t for t in self.limiter.requests[client_ip]
            if t > time.time() - 60
        ])
        hour_remaining = self.limiter.requests_per_hour - len([
            t for t in self.limiter.requests[client_ip]
            if t > time.time() - 3600
        ])
        
        response.headers["X-RateLimit-Limit-Minute"] = str(self.limiter.requests_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(minute_remaining)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.limiter.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Hour"] = str(hour_remaining)
        
        return response 