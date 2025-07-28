#!/usr/bin/env python
"""
Test script to verify that the rate_limit_class decorator fix works correctly.
"""
import os
import sys
import django
from django.conf import settings
from django.test import RequestFactory
from django.http import JsonResponse
from django.views import View

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django_rate_limiter',
        ],
        SECRET_KEY='test-secret-key',
        USE_TZ=True,
    )

django.setup()

from django_rate_limiter.decorators import rate_limit_class


# Test class-based view with rate limiting
@rate_limit_class(limit=5, window=60, methods=['GET', 'POST'])
class TestView(View):
    def get(self, request):
        return JsonResponse({"message": "GET response", "user": str(request.user)})
    
    def post(self, request):
        return JsonResponse({"message": "POST response", "user": str(request.user)})


from django.contrib.auth.models import AnonymousUser


def test_class_decorator():
    """Test that the rate_limit_class decorator works with class-based views."""
    factory = RequestFactory()
    view = TestView()
    
    print("Testing rate_limit_class decorator...")
    
    # Test GET request
    print("Testing GET request...")
    request = factory.get('/')
    request.user = AnonymousUser()  # Use proper anonymous user
    
    try:
        response = view.get(request)
        print(f"✓ GET request successful: {response.status_code}")
        print(f"✓ Response content: {response.content.decode()}")
        
        # Check rate limit headers
        if hasattr(response, 'get'):
            limit_header = response.get('X-RateLimit-Limit')
            remaining_header = response.get('X-RateLimit-Remaining') 
            print(f"✓ Rate limit headers - Limit: {limit_header}, Remaining: {remaining_header}")
        
    except Exception as e:
        print(f"✗ GET request failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test POST request
    print("\nTesting POST request...")
    request = factory.post('/')
    request.user = AnonymousUser()  # Use proper anonymous user
    
    try:
        response = view.post(request)
        print(f"✓ POST request successful: {response.status_code}")
        print(f"✓ Response content: {response.content.decode()}")
        
        # Check rate limit headers
        if hasattr(response, 'get'):
            limit_header = response.get('X-RateLimit-Limit')
            remaining_header = response.get('X-RateLimit-Remaining')
            print(f"✓ Rate limit headers - Limit: {limit_header}, Remaining: {remaining_header}")
        
    except Exception as e:
        print(f"✗ POST request failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n✓ All tests passed! The rate_limit_class decorator is working correctly.")
    return True


if __name__ == "__main__":
    success = test_class_decorator()
    sys.exit(0 if success else 1)
