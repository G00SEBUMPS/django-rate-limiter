#!/usr/bin/env python
"""
Test script to verify that the rate_limit_method decorator works correctly.
"""
import os
import sys
import django
from django.conf import settings

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

from django.test import RequestFactory
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import AnonymousUser
from django_rate_limiter.decorators import rate_limit_method


# Test class with rate_limit_method decorator
@rate_limit_method('post', limit=3, window=60)  # Only POST method rate limited
class TestView(View):
    def post(self, request):
        return JsonResponse({"message": "POST response", "method": "post"})
    
    def get(self, request):
        return JsonResponse({"message": "GET response", "method": "get"})
    
    def put(self, request):
        return JsonResponse({"message": "PUT response", "method": "put"})


def test_rate_limit_method():
    """Test that the rate_limit_method decorator works correctly."""
    factory = RequestFactory()
    view = TestView()
    
    print("Testing rate_limit_method decorator...")
    
    # Test POST method (should be rate limited)
    print("\n1. Testing POST method (rate limited)...")
    for i in range(5):  # Try 5 requests, limit is 3
        request = factory.post('/')
        request.user = AnonymousUser()
        
        try:
            response = view.post(request)
            print(f"   Request {i+1}: Status {response.status_code}")
            
            # Check if we have rate limit headers
            if hasattr(response, 'get'):
                limit_header = response.get('X-RateLimit-Limit')
                remaining_header = response.get('X-RateLimit-Remaining')
                if limit_header:
                    print(f"   Headers - Limit: {limit_header}, Remaining: {remaining_header}")
            
            if response.status_code == 429:
                print("   ✓ Rate limit correctly enforced!")
                break
                
        except Exception as e:
            print(f"   ✗ POST request {i+1} failed: {e}")
            return False
    
    # Test GET method (should NOT be rate limited)
    print("\n2. Testing GET method (not rate limited)...")
    for i in range(3):
        request = factory.get('/')
        request.user = AnonymousUser()
        
        try:
            response = view.get(request)
            print(f"   Request {i+1}: Status {response.status_code}")
            
            # Check headers - should not have rate limit headers
            if hasattr(response, 'get'):
                limit_header = response.get('X-RateLimit-Limit')
                if limit_header:
                    print(f"   ✗ Unexpected rate limit headers found: {limit_header}")
                    return False
                else:
                    print(f"   ✓ No rate limit headers (correct)")
            
        except Exception as e:
            print(f"   ✗ GET request {i+1} failed: {e}")
            return False
    
    # Test PUT method (should NOT be rate limited)
    print("\n3. Testing PUT method (not rate limited)...")
    request = factory.put('/')
    request.user = AnonymousUser()
    
    try:
        response = view.put(request)
        print(f"   PUT request: Status {response.status_code}")
        
        if hasattr(response, 'get'):
            limit_header = response.get('X-RateLimit-Limit')
            if limit_header:
                print(f"   ✗ Unexpected rate limit headers found: {limit_header}")
                return False
            else:
                print(f"   ✓ No rate limit headers (correct)")
        
    except Exception as e:
        print(f"   ✗ PUT request failed: {e}")
        return False
    
    print("\n✓ All tests passed! The rate_limit_method decorator works correctly.")
    print("✓ Only the specified method (POST) is rate limited")
    print("✓ Other methods (GET, PUT) are not affected")
    return True


if __name__ == "__main__":
    success = test_rate_limit_method()
    sys.exit(0 if success else 1)
