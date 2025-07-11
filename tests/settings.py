"""
Test configuration for Django Rate Limiter tests.
"""

SECRET_KEY = "test-secret-key-for-django-rate-limiter"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django_rate_limiter",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

USE_TZ = True

# Rate limiting settings for tests
RATE_LIMIT_SETTINGS = {
    "BACKEND": "memory",
    "DEFAULT_ALGORITHM": "sliding_window",
    "RULES": [
        {
            "path_pattern": r"^/api/",
            "limit": 10,
            "window": 60,
            "algorithm": "sliding_window",
            "scope": "api",
        },
        {
            "path_pattern": r"^/login/$",
            "limit": 5,
            "window": 300,
            "algorithm": "fixed_window",
            "use_user": False,
        },
    ],
    "GLOBAL_LIMIT": 100,
    "GLOBAL_WINDOW": 3600,
    "EXEMPT_PATHS": [r"^/health/$"],
    "EXEMPT_IPS": ["127.0.0.1"],
    "USE_USER_ID": True,
    "RATE_LIMIT_HEADERS": True,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_rate_limiter.middleware.RateLimitMiddleware",
]

ROOT_URLCONF = "tests.urls"
