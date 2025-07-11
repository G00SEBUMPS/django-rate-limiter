#!/usr/bin/env python3
"""
Configuration Examples for Django Rate Limiter Storage Backends

This script demonstrates how to configure and use different storage backends:
- In-Memory (default)
- Database (persistent)
- Redis (distributed)
"""

import os
import sys

import django
from django.conf import settings

# Configure Django settings for this example
if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django_rate_limiter",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        USE_TZ=True,
        # Rate limiting configuration examples
        RATE_LIMIT_SETTINGS={
            "BACKEND": "memory",  # Can be 'memory', 'database', or 'redis'
            "DEFAULT_ALGORITHM": "sliding_window",
            "GLOBAL_LIMIT": 100,
            "GLOBAL_WINDOW": 3600,
            "RATE_LIMIT_HEADERS": True,
        },
    )

django.setup()

from django_rate_limiter.algorithms import get_rate_limiter
from django_rate_limiter.backends import (
    DatabaseBackend,
    MemoryBackend,
    RedisBackend,
    get_backend,
)
from django_rate_limiter.decorators import rate_limit
from django_rate_limiter.exceptions import BackendError, RateLimitExceeded


def demo_memory_backend():
    """Demonstrate in-memory storage backend."""
    print("=== MEMORY BACKEND DEMO ===")
    print("Best for: Development, single process, fast operations")

    # Method 1: Direct instantiation
    backend = MemoryBackend()
    rate_limiter = get_rate_limiter("sliding_window", backend=backend)

    print("\nTesting memory backend with sliding window...")
    for i in range(6):
        try:
            allowed, metadata = rate_limiter.is_allowed("user1", limit=3, window=60)
            if allowed:
                print(
                    f"Request {i+1}: ✅ ALLOWED - Remaining: {metadata.get('remaining', 0)}"
                )
            else:
                print(
                    f"Request {i+1}: ❌ DENIED - Retry after: {metadata.get('retry_after', 0)}s"
                )
        except Exception as e:
            print(f"Request {i+1}: ❌ ERROR - {e}")

    # Method 2: Using factory function
    memory_backend = get_backend("memory")
    print(f"\nBackend type: {type(memory_backend).__name__}")

    # Memory backend configuration in settings would be:
    print("\n📝 Configuration in Django settings.py:")
    print(
        """
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'memory',
    'DEFAULT_ALGORITHM': 'sliding_window',
    'GLOBAL_LIMIT': 1000,
    'GLOBAL_WINDOW': 3600,
}
"""
    )


def demo_database_backend():
    """Demonstrate database storage backend."""
    print("\n=== DATABASE BACKEND DEMO ===")
    print("Best for: Persistence across restarts, single/multiple processes")

    try:
        # Method 1: Direct instantiation
        backend = DatabaseBackend()
        rate_limiter = get_rate_limiter("fixed_window", backend=backend)

        print("\nTesting database backend with fixed window...")
        for i in range(4):
            try:
                allowed, metadata = rate_limiter.is_allowed("user2", limit=2, window=60)
                if allowed:
                    print(
                        f"Request {i+1}: ✅ ALLOWED - Remaining: {metadata.get('remaining', 0)}"
                    )
                else:
                    print(
                        f"Request {i+1}: ❌ DENIED - Reset time: {metadata.get('reset_time', 0)}"
                    )
            except Exception as e:
                print(f"Request {i+1}: ❌ ERROR - {e}")

        # Method 2: Using factory function
        db_backend = get_backend("database")
        print(f"\nBackend type: {type(db_backend).__name__}")

        print("\n📝 Configuration in Django settings.py:")
        print(
            """
INSTALLED_APPS = [
    # ... your apps
    'django_rate_limiter',
]

RATE_LIMIT_SETTINGS = {
    'BACKEND': 'database',
    'DEFAULT_ALGORITHM': 'sliding_window',
    'GLOBAL_LIMIT': 1000,
    'GLOBAL_WINDOW': 3600,
}

# Run migrations:
# python manage.py migrate django_rate_limiter

# Optional cleanup command:
# python manage.py cleanup_rate_limits
"""
        )

    except Exception as e:
        print(f"❌ Database backend error: {e}")
        print("Note: Database backend requires Django models to be migrated")


def demo_redis_backend():
    """Demonstrate Redis storage backend."""
    print("\n=== REDIS BACKEND DEMO ===")
    print("Best for: High performance, distributed systems, multiple processes")

    try:
        # Method 1: Direct instantiation with connection parameters
        backend = RedisBackend(host="localhost", port=6379, db=0)
        rate_limiter = get_rate_limiter("token_bucket", backend=backend)

        print("\nTesting Redis backend with token bucket...")
        for i in range(5):
            try:
                allowed, metadata = rate_limiter.is_allowed(
                    "user3", limit=10, window=60, burst_capacity=3
                )
                if allowed:
                    tokens = metadata.get("remaining_tokens", 0)
                    print(f"Request {i+1}: ✅ ALLOWED - Remaining tokens: {tokens:.1f}")
                else:
                    retry_after = metadata.get("retry_after", 0)
                    print(f"Request {i+1}: ❌ DENIED - Retry after: {retry_after}s")
            except Exception as e:
                print(f"Request {i+1}: ❌ ERROR - {e}")

        # Method 2: Using factory function
        redis_backend = get_backend("redis", host="localhost", port=6379, db=0)
        print(f"\nBackend type: {type(redis_backend).__name__}")

    except BackendError as e:
        print(f"❌ Redis backend error: {e}")
        print("Note: Redis backend requires 'redis' package and running Redis server")
        print("Install with: pip install redis")
        print("Start Redis: redis-server")
    except Exception as e:
        print(f"❌ Redis connection error: {e}")
        print("Make sure Redis server is running on localhost:6379")

    print("\n📝 Configuration in Django settings.py:")
    print(
        """
# Method 1: Basic Redis configuration
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'redis',
    'BACKEND_KWARGS': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None,  # Set if Redis has auth
    },
    'DEFAULT_ALGORITHM': 'sliding_window',
    'GLOBAL_LIMIT': 1000,
    'GLOBAL_WINDOW': 3600,
}

# Method 2: Using Redis URL
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'redis',
    'BACKEND_KWARGS': {
        'host': 'redis://localhost:6379/0',
    },
}

# Method 3: Using existing Redis client
import redis
REDIS_CLIENT = redis.Redis(host='localhost', port=6379, db=0)

RATE_LIMIT_SETTINGS = {
    'BACKEND': 'redis',
    'BACKEND_KWARGS': {
        'redis_client': REDIS_CLIENT,
    },
}

# Method 4: Production with environment variables
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'redis',
    'BACKEND_KWARGS': {
        'host': os.environ.get('REDIS_HOST', 'localhost'),
        'port': int(os.environ.get('REDIS_PORT', 6379)),
        'password': os.environ.get('REDIS_PASSWORD'),
        'db': int(os.environ.get('REDIS_DB', 0)),
    },
}
"""
    )


def demo_decorator_usage():
    """Demonstrate using decorators with different backends."""
    print("\n=== DECORATOR USAGE WITH BACKENDS ===")

    # Mock Django request object for demonstration
    class MockRequest:
        def __init__(self, user_id=None, ip="127.0.0.1"):
            self.META = {"REMOTE_ADDR": ip}
            if user_id:
                from types import SimpleNamespace

                self.user = SimpleNamespace(is_authenticated=True, pk=user_id)
            else:
                self.user = SimpleNamespace(is_authenticated=False)

    # Example decorator usage (would normally be on Django views)
    print("\n📝 Decorator examples:")
    print(
        """
# Using default backend from settings
@rate_limit(limit=100, window=3600)
def my_view(request):
    return JsonResponse({"message": "Hello"})

# Explicitly specify memory backend
@rate_limit(limit=100, window=3600, backend="memory")
def fast_view(request):
    return JsonResponse({"message": "Fast"})

# Database backend for persistence
@rate_limit(limit=50, window=300, backend="database")
def persistent_view(request):
    return JsonResponse({"message": "Persistent"})

# Redis backend with custom configuration
@rate_limit(
    limit=1000, 
    window=3600, 
    backend="redis",
    backend_kwargs={'host': 'localhost', 'port': 6379}
)
def distributed_view(request):
    return JsonResponse({"message": "Distributed"})

# Different algorithms with different backends
@rate_limit(limit=10, window=60, algorithm="token_bucket", backend="memory")
def burst_view(request):
    return JsonResponse({"message": "Burst allowed"})

@rate_limit(limit=5, window=300, algorithm="fixed_window", backend="database")
def strict_view(request):
    return JsonResponse({"message": "Strict limits"})
"""
    )


def demo_programmatic_usage():
    """Demonstrate programmatic usage with different backends."""
    print("\n=== PROGRAMMATIC USAGE ===")

    from django_rate_limiter.utils import check_rate_limit, is_rate_limited

    backends_to_test = ["memory"]  # Only test memory for this demo

    for backend_name in backends_to_test:
        print(f"\nTesting {backend_name} backend programmatically...")

        try:
            # Test rate limiting
            for i in range(3):
                try:
                    metadata = check_rate_limit(
                        identifier="prog_user",
                        limit=2,
                        window=60,
                        backend=backend_name,
                        algorithm="sliding_window",
                    )
                    print(
                        f"  Request {i+1}: ✅ SUCCESS - Remaining: {metadata.get('remaining', 0)}"
                    )
                except RateLimitExceeded as e:
                    print(f"  Request {i+1}: ❌ RATE LIMITED - {e}")

            # Check status without making request
            is_limited = is_rate_limited(
                identifier="prog_user", limit=2, window=60, backend=backend_name
            )
            print(f"  Is 'prog_user' rate limited? {is_limited}")

        except Exception as e:
            print(f"  ❌ Error with {backend_name} backend: {e}")


def show_performance_characteristics():
    """Show performance characteristics of different backends."""
    print("\n=== PERFORMANCE CHARACTERISTICS ===")

    characteristics = {
        "Memory": {
            "Speed": "⭐⭐⭐⭐⭐ (Fastest)",
            "Persistence": "❌ (Lost on restart)",
            "Multi-Process": "❌ (Single process only)",
            "Scalability": "⭐ (Limited)",
            "Setup": "⭐⭐⭐⭐⭐ (No setup needed)",
            "Use Case": "Development, single server, temporary limits",
        },
        "Database": {
            "Speed": "⭐⭐⭐ (Good)",
            "Persistence": "⭐⭐⭐⭐⭐ (Fully persistent)",
            "Multi-Process": "⭐⭐⭐⭐⭐ (Shared across processes)",
            "Scalability": "⭐⭐⭐ (Database dependent)",
            "Setup": "⭐⭐⭐⭐ (Run migrations)",
            "Use Case": "Production, persistent limits, existing DB infrastructure",
        },
        "Redis": {
            "Speed": "⭐⭐⭐⭐⭐ (Very fast)",
            "Persistence": "⭐⭐⭐⭐⭐ (Configurable persistence)",
            "Multi-Process": "⭐⭐⭐⭐⭐ (Distributed)",
            "Scalability": "⭐⭐⭐⭐⭐ (Highly scalable)",
            "Setup": "⭐⭐⭐ (Requires Redis server)",
            "Use Case": "High traffic, distributed systems, microservices",
        },
    }

    for backend, chars in characteristics.items():
        print(f"\n{backend} Backend:")
        for aspect, rating in chars.items():
            print(f"  {aspect:15}: {rating}")


if __name__ == "__main__":
    print("Django Rate Limiter - Storage Backend Configuration Examples")
    print("=" * 70)

    try:
        demo_memory_backend()
        demo_database_backend()
        demo_redis_backend()
        demo_decorator_usage()
        demo_programmatic_usage()
        show_performance_characteristics()

        print("\n" + "=" * 70)
        print("✅ Configuration examples completed!")
        print("\nChoose the backend that best fits your needs:")
        print("- Memory: Fast, simple, development")
        print("- Database: Persistent, reliable, single server")
        print("- Redis: Fast, distributed, high traffic")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
