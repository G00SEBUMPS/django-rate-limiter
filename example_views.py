"""
Example Django views showing rate limiter configuration with different backends.

This demonstrates how to integrate the Django Rate Limiter in a real Django project.
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django_rate_limiter.decorators import (
    rate_limit,
    throttle,
    per_user_rate_limit,
    per_ip_rate_limit,
    custom_key_rate_limit,
)


# =============================================================================
# MEMORY BACKEND EXAMPLES (Development)
# =============================================================================


@rate_limit(limit=10, window=60, backend="memory")
def api_memory_endpoint(request):
    """API endpoint using memory backend - fast but not persistent."""
    return JsonResponse(
        {
            "message": "Memory backend response",
            "backend": "memory",
            "persistent": False,
            "good_for": "development, testing",
        }
    )


@throttle("100/hour", backend="memory")
def memory_throttled_view(request):
    """View with memory backend using throttle decorator."""
    return JsonResponse(
        {"message": "Throttled with memory backend", "rate": "100 requests per hour"}
    )


# =============================================================================
# DATABASE BACKEND EXAMPLES (Single Server Production)
# =============================================================================


@rate_limit(limit=50, window=300, backend="database", algorithm="fixed_window")
def api_database_endpoint(request):
    """API endpoint using database backend - persistent across restarts."""
    return JsonResponse(
        {
            "message": "Database backend response",
            "backend": "database",
            "persistent": True,
            "good_for": "single server production",
        }
    )


@per_user_rate_limit(limit=1000, window=3600, backend="database")
@login_required
def user_dashboard(request):
    """User dashboard with per-user rate limiting using database."""
    return JsonResponse(
        {
            "user": str(request.user),
            "message": "Dashboard data",
            "rate_limit": "1000 requests per hour per user",
        }
    )


# =============================================================================
# REDIS BACKEND EXAMPLES (Distributed Production)
# =============================================================================


@rate_limit(
    limit=1000,
    window=3600,
    backend="redis",
    backend_kwargs={"host": "localhost", "port": 6379, "db": 0},
    algorithm="sliding_window",
)
def api_redis_endpoint(request):
    """API endpoint using Redis backend - high performance, distributed."""
    return JsonResponse(
        {
            "message": "Redis backend response",
            "backend": "redis",
            "persistent": True,
            "distributed": True,
            "good_for": "high traffic, multiple servers",
        }
    )


@rate_limit(
    limit=500, window=60, backend="redis", algorithm="token_bucket", scope="api_v2"
)
def api_v2_endpoint(request):
    """API v2 with token bucket algorithm using Redis."""
    return JsonResponse(
        {"version": "v2", "algorithm": "token_bucket", "allows_bursts": True}
    )


# =============================================================================
# CUSTOM KEY FUNCTIONS
# =============================================================================


def extract_api_key(request):
    """Extract API key from request headers."""
    return request.META.get("HTTP_X_API_KEY", "anonymous")


@custom_key_rate_limit(
    key_func=extract_api_key,
    limit=10000,
    window=3600,
    backend="redis",
    scope="api_keys",
)
def api_key_endpoint(request):
    """Rate limit by API key instead of user/IP."""
    api_key = request.META.get("HTTP_X_API_KEY", "None")
    return JsonResponse(
        {
            "api_key": api_key[:8] + "..." if api_key != "None" else "None",
            "message": "API key based rate limiting",
        }
    )


# =============================================================================
# IP-BASED RATE LIMITING
# =============================================================================


@per_ip_rate_limit(limit=5, window=300, backend="memory")
def login_endpoint(request):
    """Login endpoint with strict IP-based rate limiting."""
    if request.method == "POST":
        # Login logic here...
        return JsonResponse({"status": "login_attempt"})
    return JsonResponse({"method": "POST required"})


# =============================================================================
# MIXED BACKEND STRATEGY
# =============================================================================


def get_backend_for_endpoint(endpoint_type):
    """Dynamic backend selection based on endpoint type."""
    from django.conf import settings

    if settings.DEBUG:
        return "memory"  # Fast for development

    backend_map = {
        "auth": "database",  # Persistent for authentication
        "api": "redis",  # Fast for API calls
        "uploads": "database",  # Persistent for file operations
    }

    return backend_map.get(endpoint_type, "memory")


@rate_limit(
    limit=100,
    window=3600,
    backend=get_backend_for_endpoint("api"),
    algorithm="sliding_window",
)
def smart_api_endpoint(request):
    """API that chooses backend based on environment and type."""
    from django.conf import settings

    backend_used = get_backend_for_endpoint("api")

    return JsonResponse(
        {
            "message": "Smart backend selection",
            "backend_used": backend_used,
            "debug_mode": settings.DEBUG,
        }
    )


# =============================================================================
# PROGRAMMATIC RATE LIMITING
# =============================================================================

from django_rate_limiter.utils import check_rate_limit, is_rate_limited
from django_rate_limiter.exceptions import RateLimitExceeded


def manual_rate_check_view(request):
    """Example of manual rate limiting check."""
    user_id = (
        str(request.user.id)
        if request.user.is_authenticated
        else request.META.get("REMOTE_ADDR")
    )

    try:
        # Check rate limit without decorators
        metadata = check_rate_limit(
            identifier=f"manual:{user_id}",
            limit=20,
            window=300,  # 5 minutes
            backend="memory",
            algorithm="fixed_window",
        )

        return JsonResponse(
            {
                "allowed": True,
                "remaining": metadata.get("remaining", 0),
                "reset_time": metadata.get("reset_time", 0),
                "message": "Manual rate check passed",
            }
        )

    except RateLimitExceeded as e:
        return JsonResponse(
            {
                "allowed": False,
                "error": str(e),
                "retry_after": e.retry_after,
                "message": "Manual rate check failed",
            },
            status=429,
        )


def check_status_view(request):
    """Check rate limit status without affecting the count."""
    from django_rate_limiter.utils import get_rate_limit_status

    user_id = (
        str(request.user.id)
        if request.user.is_authenticated
        else request.META.get("REMOTE_ADDR")
    )

    status = get_rate_limit_status(
        identifier=f"status:{user_id}", limit=100, window=3600, backend="memory"
    )

    return JsonResponse(
        {
            "current_count": status.get("current_count", 0),
            "remaining": status.get("remaining", 0),
            "limit": status.get("limit", 0),
            "is_limited": status.get("is_limited", False),
            "message": "Rate limit status check",
        }
    )


# =============================================================================
# SETTINGS EXAMPLES FOR DIFFERENT SCENARIOS
# =============================================================================

"""
# Example settings.py configurations:

# 1. DEVELOPMENT SETUP (settings/development.py)
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'memory',
    'DEFAULT_ALGORITHM': 'sliding_window',
    'GLOBAL_LIMIT': 10000,  # Generous limits for development
    'GLOBAL_WINDOW': 3600,
    'RATE_LIMIT_HEADERS': True,
}

# 2. SINGLE SERVER PRODUCTION (settings/production.py)
RATE_LIMIT_SETTINGS = {
    'BACKEND': 'database',
    'DEFAULT_ALGORITHM': 'sliding_window',
    'GLOBAL_LIMIT': 1000,
    'GLOBAL_WINDOW': 3600,
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
    'EXEMPT_PATHS': [r'^/health/$', r'^/static/'],
    'RATE_LIMIT_HEADERS': True,
}

# 3. DISTRIBUTED PRODUCTION (settings/production.py)
import os

RATE_LIMIT_SETTINGS = {
    'BACKEND': 'redis',
    'BACKEND_KWARGS': {
        'host': os.environ.get('REDIS_HOST', 'localhost'),
        'port': int(os.environ.get('REDIS_PORT', 6379)),
        'password': os.environ.get('REDIS_PASSWORD'),
        'db': int(os.environ.get('REDIS_DB', 0)),
    },
    'DEFAULT_ALGORITHM': 'sliding_window',
    'GLOBAL_LIMIT': 5000,
    'GLOBAL_WINDOW': 3600,
    'RULES': [
        {
            'path_pattern': r'^/api/v1/',
            'limit': 1000,
            'window': 3600,
            'algorithm': 'sliding_window',
            'scope': 'api_v1',
        },
        {
            'path_pattern': r'^/api/v2/',
            'limit': 2000,
            'window': 3600,
            'algorithm': 'token_bucket',
            'scope': 'api_v2',
        },
    ],
    'RATE_LIMIT_HEADERS': True,
}

# 4. MIDDLEWARE SETUP
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_rate_limiter.middleware.RateLimitMiddleware',  # Add this
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 5. CELERY TASK FOR CLEANUP (with database backend)
# In your celery tasks:
from celery import shared_task
from django_rate_limiter.utils import cleanup_expired_entries

@shared_task
def cleanup_rate_limits():
    '''Clean up expired rate limit entries (run hourly)'''
    deleted_count = cleanup_expired_entries()
    return f"Deleted {deleted_count} expired rate limit entries"
"""
