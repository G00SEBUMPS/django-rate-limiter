# Django Rate Limiter Configuration Guide

This guide explains how to configure the Django Rate Limiter to use different storage backends: in-memory, database, or Redis.

## 1. Installation

First, install the package:

```bash
pip install django-rate-limiter
```

For Redis support, also install:
```bash
pip install redis
```

## 2. Django Settings Configuration

Add the app to your Django `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [
    # ... your other apps
    'django_rate_limiter',
]
```

## 3. Storage Backend Configuration

### 3.1 In-Memory Storage (Default)

The simplest configuration - no additional setup required:

```python
# settings.py
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'memory',  # Default
    'DEFAULT_ALGORITHM': 'sliding_window',
    'GLOBAL_LIMIT': 1000,
    'GLOBAL_WINDOW': 3600,  # 1 hour
}
```

**Pros:** Fast, no external dependencies
**Cons:** Data lost on restart, not shared across multiple processes

### 3.2 Database Storage

Uses Django's database for persistent storage:

```python
# settings.py
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'database',
    'DEFAULT_ALGORITHM': 'sliding_window',
    'GLOBAL_LIMIT': 1000,
    'GLOBAL_WINDOW': 3600,
}
```

**Setup steps:**
1. Run migrations to create the rate limit table:
   ```bash
   python manage.py migrate django_rate_limiter
   ```

2. Optional: Set up periodic cleanup (add to cron or Celery):
   ```bash
   python manage.py cleanup_rate_limits
   ```

**Pros:** Persistent, works across processes, no external dependencies
**Cons:** Slower than memory/Redis, database queries

### 3.3 Redis Storage

High-performance distributed storage:

```python
# settings.py
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'redis',
    'BACKEND_KWARGS': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None,  # Set if Redis has auth
        'decode_responses': True,
    },
    'DEFAULT_ALGORITHM': 'sliding_window',
    'GLOBAL_LIMIT': 1000,
    'GLOBAL_WINDOW': 3600,
}
```

**Alternative Redis configurations:**

Using Redis URL:
```python
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'redis',
    'BACKEND_KWARGS': {
        'host': 'redis://localhost:6379/0',
    },
}
```

Using existing Redis connection:
```python
import redis

REDIS_CLIENT = redis.Redis(host='localhost', port=6379, db=0)

RATE_LIMIT_SETTINGS = {
    'BACKEND': 'redis',
    'BACKEND_KWARGS': {
        'redis_client': REDIS_CLIENT,
    },
}
```

**Pros:** Very fast, persistent, distributed, scales across multiple servers
**Cons:** Requires Redis server

## 4. Using Different Backends in Code

### 4.1 With Decorators

```python
from django_rate_limiter.decorators import rate_limit

# Using default backend from settings
@rate_limit(limit=100, window=3600)
def my_view(request):
    return JsonResponse({"message": "Hello"})

# Explicitly specify backend
@rate_limit(limit=100, window=3600, backend="memory")
def fast_view(request):
    return JsonResponse({"message": "Fast"})

@rate_limit(limit=50, window=300, backend="database")
def persistent_view(request):
    return JsonResponse({"message": "Persistent"})

@rate_limit(
    limit=1000, 
    window=3600, 
    backend="redis",
    backend_kwargs={'host': 'localhost', 'port': 6379}
)
def distributed_view(request):
    return JsonResponse({"message": "Distributed"})
```

### 4.2 Programmatically

```python
from django_rate_limiter.utils import check_rate_limit
from django_rate_limiter.backends import get_backend
from django_rate_limiter.algorithms import get_rate_limiter

# Using utility function
try:
    check_rate_limit(
        identifier="user:123",
        limit=100,
        window=3600,
        backend="redis"  # or "memory", "database"
    )
except RateLimitExceeded:
    print("Rate limited!")

# Using backends directly
memory_backend = get_backend("memory")
db_backend = get_backend("database")
redis_backend = get_backend("redis", host="localhost", port=6379)

# Create rate limiter with specific backend
rate_limiter = get_rate_limiter(
    algorithm="sliding_window",
    backend=redis_backend
)
```

## 5. Middleware Configuration

Configure automatic rate limiting for all requests:

```python
# settings.py
MIDDLEWARE = [
    # ... other middleware
    'django_rate_limiter.middleware.RateLimitMiddleware',
]

RATE_LIMIT_SETTINGS = {
    'BACKEND': 'redis',  # or 'memory', 'database'
    'BACKEND_KWARGS': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    },
    'DEFAULT_ALGORITHM': 'sliding_window',
    'RULES': [
        {
            'path_pattern': r'^/api/',
            'limit': 1000,
            'window': 3600,
            'algorithm': 'sliding_window',
            'scope': 'api',
        },
        {
            'path_pattern': r'^/auth/login/$',
            'limit': 5,
            'window': 300,
            'algorithm': 'fixed_window',
            'use_user': False,  # Rate limit by IP
        },
    ],
    'GLOBAL_LIMIT': 10000,
    'GLOBAL_WINDOW': 3600,
    'EXEMPT_PATHS': [r'^/health/$', r'^/static/'],
    'EXEMPT_IPS': ['127.0.0.1'],
    'USE_USER_ID': True,
    'RATE_LIMIT_HEADERS': True,
}
```

## 6. Environment-Specific Configuration

### Development (local)
```python
# settings/development.py
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'memory',  # Simple for development
    'GLOBAL_LIMIT': 10000,  # Generous limits
    'GLOBAL_WINDOW': 3600,
}
```

### Testing
```python
# settings/testing.py
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'memory',  # Fast for tests
    'GLOBAL_LIMIT': 1000000,  # Very high limits
    'GLOBAL_WINDOW': 1,
}
```

### Production
```python
# settings/production.py
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'redis',  # Scalable for production
    'BACKEND_KWARGS': {
        'host': os.environ.get('REDIS_HOST', 'localhost'),
        'port': int(os.environ.get('REDIS_PORT', 6379)),
        'password': os.environ.get('REDIS_PASSWORD'),
        'db': int(os.environ.get('REDIS_DB', 0)),
    },
    'DEFAULT_ALGORITHM': 'sliding_window',
    'GLOBAL_LIMIT': 1000,
    'GLOBAL_WINDOW': 3600,
}
```

## 7. Performance Comparison

| Backend  | Speed | Persistence | Multi-Process | Scalability | Setup |
|----------|-------|-------------|---------------|-------------|-------|
| Memory   | ⭐⭐⭐⭐⭐ | ❌ | ❌ | ⭐ | ⭐⭐⭐⭐⭐ |
| Database | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Redis    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 8. Best Practices

1. **Development**: Use memory backend for simplicity
2. **Production with single server**: Database backend for persistence
3. **Production with multiple servers**: Redis backend for distributed rate limiting
4. **High traffic**: Redis backend with clustering
5. **Mixed workloads**: Use different backends for different endpoints

## 9. Troubleshooting

### Memory Backend Issues
- Data loss on restart is expected
- Not shared between processes

### Database Backend Issues
- Ensure migrations are run: `python manage.py migrate django_rate_limiter`
- Clean up expired entries: `python manage.py cleanup_rate_limits`
- Check database performance for high-traffic scenarios

### Redis Backend Issues
- Verify Redis connection: `redis-cli ping`
- Check Redis configuration for persistence
- Monitor Redis memory usage
- Consider Redis clustering for high availability

## 10. Example: Dynamic Backend Selection

```python
# utils.py
def get_rate_limit_backend():
    """Dynamically select backend based on environment."""
    if settings.DEBUG:
        return "memory"
    elif settings.TESTING:
        return "memory" 
    else:
        return "redis"

# views.py
@rate_limit(
    limit=100, 
    window=3600, 
    backend=get_rate_limit_backend()
)
def my_view(request):
    return JsonResponse({"message": "Hello"})
```

This configuration guide covers all the ways to set up and use different storage backends with the Django Rate Limiter package.
