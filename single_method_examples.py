"""
Examples showing different ways to apply rate limiting to specific methods.
"""

from django.http import JsonResponse
from django.views import View
from django_rate_limiter.decorators import (
    rate_limit, 
    rate_limit_class, 
    rate_limit_method
)

# Option 1: Using @rate_limit directly on a specific method
class Option1View(View):
    @rate_limit(limit=50, window=3600)  # Only rate limit POST
    def post(self, request):
        return JsonResponse({"message": "POST is rate limited"})
    
    def get(self, request):
        # Not rate limited
        return JsonResponse({"message": "GET is not rate limited"})
    
    def put(self, request):
        # Not rate limited
        return JsonResponse({"message": "PUT is not rate limited"})


# Option 2: Using @rate_limit_class with specific methods parameter
@rate_limit_class(limit=50, window=3600, methods=['POST'])  # Only POST
class Option2View(View):
    def post(self, request):
        # Rate limited
        return JsonResponse({"message": "POST is rate limited"})
    
    def get(self, request):
        # Not rate limited
        return JsonResponse({"message": "GET is not rate limited"})
    
    def put(self, request):
        # Not rate limited  
        return JsonResponse({"message": "PUT is not rate limited"})


# Option 3: Using the new @rate_limit_method decorator
@rate_limit_method('post', limit=50, window=3600)  # Only POST method
class Option3View(View):
    def post(self, request):
        # Rate limited
        return JsonResponse({"message": "POST is rate limited"})
    
    def get(self, request):
        # Not rate limited
        return JsonResponse({"message": "GET is not rate limited"})
    
    def put(self, request):
        # Not rate limited
        return JsonResponse({"message": "PUT is not rate limited"})


# You can also combine multiple rate limiting decorators for different methods
class CombinedView(View):
    @rate_limit(limit=100, window=3600)  # GET has different limits
    def get(self, request):
        return JsonResponse({"message": "GET with its own rate limit"})
    
    @rate_limit(limit=20, window=1800)   # POST has different limits
    def post(self, request):
        return JsonResponse({"message": "POST with its own rate limit"})
    
    def put(self, request):
        # Not rate limited at all
        return JsonResponse({"message": "PUT is not rate limited"})


# Using multiple @rate_limit_method decorators
@rate_limit_method('get', limit=100, window=3600)
@rate_limit_method('post', limit=20, window=1800)
class MultipleMethodsView(View):
    def get(self, request):
        # Rate limited: 100 requests per hour
        return JsonResponse({"message": "GET with rate limit"})
    
    def post(self, request):
        # Rate limited: 20 requests per 30 minutes
        return JsonResponse({"message": "POST with different rate limit"})
    
    def put(self, request):
        # Not rate limited
        return JsonResponse({"message": "PUT is not rate limited"})


if __name__ == "__main__":
    print("Examples of single method rate limiting:")
    print("\nOption 1: @rate_limit decorator directly on method")
    print("- Most straightforward")
    print("- Applied directly to the method you want to limit")
    
    print("\nOption 2: @rate_limit_class with methods=['POST']")
    print("- Use when you want class-level configuration")
    print("- Specify exactly which methods to rate limit")
    
    print("\nOption 3: @rate_limit_method('post', ...)")
    print("- New decorator specifically for single method")
    print("- Clean syntax for single method rate limiting")
    
    print("\nOption 4: Multiple decorators for different methods")
    print("- Apply different rate limits to different methods")
    print("- Mix and match as needed")
