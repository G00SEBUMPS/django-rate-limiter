"""
Django Rate Limiter

A comprehensive Django rate limiter with multiple algorithms and storage backends.
Supports sliding window, token bucket, and fixed window rate limiting with
thread-safe, deadlock-safe implementation.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .decorators import rate_limit
from .middleware import RateLimitMiddleware
from .algorithms import (
    SlidingWindowRateLimiter,
    TokenBucketRateLimiter,
    FixedWindowRateLimiter,
)
from .backends import MemoryBackend, DatabaseBackend, RedisBackend
from .exceptions import RateLimitExceeded

__all__ = [
    "rate_limit",
    "RateLimitMiddleware", 
    "SlidingWindowRateLimiter",
    "TokenBucketRateLimiter",
    "FixedWindowRateLimiter",
    "MemoryBackend",
    "DatabaseBackend", 
    "RedisBackend",
    "RateLimitExceeded",
]
