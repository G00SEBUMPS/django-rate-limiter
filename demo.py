#!/usr/bin/env python3
"""
Example script demonstrating Django Rate Limiter usage.
"""

import os
import sys
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django_rate_limiter',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_TZ=True,
    )

django.setup()

from django_rate_limiter import (
    SlidingWindowRateLimiter,
    TokenBucketRateLimiter, 
    FixedWindowRateLimiter,
    MemoryBackend,
    RateLimitExceeded
)


def demonstrate_sliding_window():
    """Demonstrate sliding window rate limiter."""
    print("=== Sliding Window Rate Limiter Demo ===")
    
    backend = MemoryBackend()
    limiter = SlidingWindowRateLimiter(backend=backend)
    
    print("Testing with limit=3, window=60 seconds")
    
    for i in range(5):
        try:
            metadata = limiter.enforce(
                identifier="user123",
                limit=3,
                window=60,
                scope="demo"
            )
            print(f"Request {i+1}: ALLOWED - Remaining: {metadata.get('remaining', 0)}")
        except RateLimitExceeded as e:
            print(f"Request {i+1}: DENIED - {e}")


def demonstrate_token_bucket():
    """Demonstrate token bucket rate limiter."""
    print("\n=== Token Bucket Rate Limiter Demo ===")
    
    backend = MemoryBackend()
    limiter = TokenBucketRateLimiter(backend=backend)
    
    print("Testing with limit=5 tokens/60s, burst_capacity=10")
    
    for i in range(12):
        try:
            allowed, metadata = limiter.is_allowed(
                identifier="user456",
                limit=5,  # 5 tokens per 60 seconds
                window=60,
                scope="demo",
                burst_capacity=10
            )
            if allowed:
                print(f"Request {i+1}: ALLOWED - Remaining tokens: {metadata.get('remaining_tokens', 0):.1f}")
            else:
                print(f"Request {i+1}: DENIED - Retry after: {metadata.get('retry_after', 0)} seconds")
                break
        except Exception as e:
            print(f"Request {i+1}: ERROR - {e}")


def demonstrate_fixed_window():
    """Demonstrate fixed window rate limiter."""
    print("\n=== Fixed Window Rate Limiter Demo ===")
    
    backend = MemoryBackend()
    limiter = FixedWindowRateLimiter(backend=backend)
    
    print("Testing with limit=4, window=60 seconds")
    
    for i in range(6):
        try:
            allowed, metadata = limiter.is_allowed(
                identifier="user789",
                limit=4,
                window=60,
                scope="demo"
            )
            if allowed:
                print(f"Request {i+1}: ALLOWED - Remaining: {metadata.get('remaining', 0)}")
            else:
                print(f"Request {i+1}: DENIED - Reset time: {metadata.get('reset_time', 0)}")
        except Exception as e:
            print(f"Request {i+1}: ERROR - {e}")


def demonstrate_programmatic_usage():
    """Demonstrate programmatic rate limiting utilities."""
    print("\n=== Programmatic Usage Demo ===")
    
    from django_rate_limiter.utils import check_rate_limit, is_rate_limited
    
    print("Testing programmatic rate limiting...")
    
    # Test successful requests
    for i in range(3):
        try:
            metadata = check_rate_limit(
                identifier="api_user",
                limit=5,
                window=60,
                algorithm="sliding_window",
                backend="memory"
            )
            print(f"API Request {i+1}: SUCCESS - Remaining: {metadata.get('remaining', 0)}")
        except RateLimitExceeded as e:
            print(f"API Request {i+1}: FAILED - {e}")
    
    # Check if rate limited without making a request
    is_limited = is_rate_limited(
        identifier="api_user",
        limit=5,
        window=60,
        algorithm="sliding_window",
        backend="memory"
    )
    print(f"Is 'api_user' currently rate limited? {is_limited}")


if __name__ == "__main__":
    print("Django Rate Limiter Package Demo")
    print("=" * 50)
    
    try:
        demonstrate_sliding_window()
        demonstrate_token_bucket()
        demonstrate_fixed_window()
        demonstrate_programmatic_usage()
        
        print("\n" + "=" * 50)
        print("Demo completed successfully!")
        print("\nThe Django Rate Limiter package is working correctly.")
        print("You can now integrate it into your Django projects!")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
