"""
URL patterns for testing.
"""

from django.urls import path
from django.http import JsonResponse


def api_view(request):
    return JsonResponse({"message": "API response"})


def login_view(request):
    return JsonResponse({"message": "Login"})


def health_view(request):
    return JsonResponse({"status": "healthy"})


urlpatterns = [
    path("api/test/", api_view, name="api_test"),
    path("login/", login_view, name="login"),
    path("health/", health_view, name="health"),
]
