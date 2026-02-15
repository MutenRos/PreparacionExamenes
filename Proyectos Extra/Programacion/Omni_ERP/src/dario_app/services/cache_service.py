"""Enterprise-grade caching service with Redis fallback to in-memory."""

from datetime import timedelta
from typing import Any, Optional
import json
import hashlib
from functools import wraps

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from dario_app.core import settings


class CacheService:
    """Enterprise caching layer with Redis or in-memory fallback."""
    
    def __init__(self):
        self._memory_cache = {}
        self._redis_client = None
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialize Redis connection if available."""
        redis_url = getattr(settings, 'redis_url', None)
        if REDIS_AVAILABLE and redis_url:
            # Validate URL scheme
            if not str(redis_url).startswith(("redis://", "rediss://")):
                print(f"Invalid Redis URL scheme '{redis_url}', using in-memory cache")
                self._redis_client = None
                return
            try:
                self._redis_client = redis.from_url(
                    redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5
                )
            except Exception as e:
                print(f"Redis connection failed, using in-memory cache: {e}")
                self._redis_client = None
    
    async def get(self, key: str) -> Optional[Any]:
        """Get cached value by key."""
        try:
            if self._redis_client:
                value = await self._redis_client.get(key)
                return json.loads(value) if value else None
            else:
                return self._memory_cache.get(key)
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = 3600
    ) -> bool:
        """Set cached value with TTL in seconds."""
        try:
            if self._redis_client:
                serialized = json.dumps(value, default=str)
                if ttl:
                    await self._redis_client.setex(key, ttl, serialized)
                else:
                    await self._redis_client.set(key, serialized)
                return True
            else:
                self._memory_cache[key] = value
                return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete cached value."""
        try:
            if self._redis_client:
                await self._redis_client.delete(key)
            else:
                self._memory_cache.pop(key, None)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern (Redis only)."""
        try:
            if self._redis_client:
                keys = await self._redis_client.keys(pattern)
                if keys:
                    return await self._redis_client.delete(*keys)
            else:
                # In-memory pattern matching
                matching = [k for k in self._memory_cache.keys() if pattern.replace('*', '') in k]
                for k in matching:
                    del self._memory_cache[k]
                return len(matching)
            return 0
        except Exception as e:
            print(f"Cache delete pattern error: {e}")
            return 0
    
    async def clear(self) -> bool:
        """Clear entire cache."""
        try:
            if self._redis_client:
                await self._redis_client.flushdb()
            else:
                self._memory_cache.clear()
            return True
        except Exception as e:
            print(f"Cache clear error: {e}")
            return False
    
    def cache_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        key_parts = [str(arg) for arg in args]
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        key_string = ":".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()


# Global cache instance
cache = CacheService()


def cached(ttl: int = 3600, key_prefix: str = ""):
    """Decorator for caching function results."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key_str = f"{key_prefix}:{func.__name__}:{cache.cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = await cache.get(cache_key_str)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            await cache.set(cache_key_str, result, ttl)
            
            return result
        return wrapper
    return decorator


async def invalidate_org_cache(org_id: int):
    """Invalidate all cache entries for an organization."""
    await cache.delete_pattern(f"org:{org_id}:*")


async def invalidate_user_cache(user_id: int):
    """Invalidate all cache entries for a user."""
    await cache.delete_pattern(f"user:{user_id}:*")
