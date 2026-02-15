"""Enterprise rate limiting middleware."""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time


class RateLimitRule:
    """Rate limit rule configuration."""
    
    def __init__(
        self,
        requests: int,
        window_seconds: int,
        scope: str = "ip"  # ip, user, org
    ):
        self.requests = requests
        self.window_seconds = window_seconds
        self.scope = scope


class RateLimiter:
    """In-memory rate limiter (use Redis in production)."""
    
    def __init__(self):
        self._requests = defaultdict(list)
        self._blocked = {}
    
    def is_allowed(
        self,
        key: str,
        rule: RateLimitRule
    ) -> tuple[bool, Optional[int]]:
        """Check if request is allowed."""
        now = time.time()
        window_start = now - rule.window_seconds
        
        # Clean old requests
        self._requests[key] = [
            req_time for req_time in self._requests[key]
            if req_time > window_start
        ]
        
        # Check if blocked
        if key in self._blocked:
            if self._blocked[key] > now:
                retry_after = int(self._blocked[key] - now)
                return False, retry_after
            else:
                del self._blocked[key]
        
        # Check rate limit
        request_count = len(self._requests[key])
        
        if request_count >= rule.requests:
            # Block for window duration
            self._blocked[key] = now + rule.window_seconds
            return False, rule.window_seconds
        
        # Allow request
        self._requests[key].append(now)
        return True, None


# Global rate limiter
rate_limiter = RateLimiter()


# Default rate limit rules
DEFAULT_RULES = {
    "global": RateLimitRule(requests=1000, window_seconds=60),  # 1000 req/min per IP
    "auth": RateLimitRule(requests=5, window_seconds=60),  # 5 login attempts/min
    "api": RateLimitRule(requests=100, window_seconds=60),  # 100 API calls/min per user
}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware."""
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Determine rate limit rule
        path = request.url.path
        
        if "/login" in path or "/signup" in path:
            rule = DEFAULT_RULES["auth"]
            key = f"auth:{client_ip}"
        elif "/api/" in path:
            rule = DEFAULT_RULES["api"]
            # Try to get user from token
            user_context = request.state.__dict__.get("user_context")
            if user_context:
                key = f"api:user:{user_context['user_id']}"
            else:
                key = f"api:ip:{client_ip}"
        else:
            rule = DEFAULT_RULES["global"]
            key = f"global:{client_ip}"
        
        # Check rate limit
        allowed, retry_after = rate_limiter.is_allowed(key, rule)
        
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Retry after {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)}
            )
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(rule.requests)
        response.headers["X-RateLimit-Remaining"] = str(
            rule.requests - len(rate_limiter._requests[key])
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(time.time() + rule.window_seconds)
        )
        
        return response
