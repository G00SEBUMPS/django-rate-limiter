"""
Pytest configuration for Django Rate Limiter tests.
"""

import os

import django
from django.conf import settings


def pytest_configure():
    """Configure Django for pytest."""
    if not settings.configured:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
        django.setup()
