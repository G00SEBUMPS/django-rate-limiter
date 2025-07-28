"""
Example demonstrating the fixed rate_limit_class decorator.

This example shows how to use the rate_limit_class decorator with Django class-based views,
particularly with DRF APIView classes, which was causing the original AttributeError.
"""

from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response

from django_rate_limiter.decorators import rate_limit_class


# Example with Django's base View class
@rate_limit_class(limit=100, window=3600, methods=['GET', 'POST'])
class MyDjangoView(View):
    def get(self, request):
        return JsonResponse({"message": "Hello from Django View"})
    
    def post(self, request):
        return JsonResponse({"message": "POST processed"})


# Example with DRF APIView class (like the one in the error)
@rate_limit_class(limit=50, window=1800, methods=['POST'])
class SummarizeInputAIApiView(APIView):
    """
    This is similar to the view that was causing the original error.
    The issue was that when rate_limit_class applied the decorator,
    it passed 'self' as the first argument instead of 'request'.
    """
    
    def post(self, request):
        # This would previously fail with:
        # AttributeError: 'SummarizeInputAIApiView' object has no attribute 'META'
        # because the decorator was treating 'self' as the request object
        return Response({"message": "AI summarization complete"})


# Example with custom methods and scope
@rate_limit_class(
    limit=200, 
    window=3600, 
    methods=['GET', 'POST', 'PUT'], 
    scope="api.custom",
    backend="memory",
    algorithm="sliding_window"
)
class CustomAPIView(APIView):
    def get(self, request):
        return Response({"data": "retrieved"})
    
    def post(self, request):
        return Response({"data": "created"})
    
    def put(self, request):
        return Response({"data": "updated"})


# Example with per-IP rate limiting
@rate_limit_class(
    limit=10, 
    window=60, 
    methods=['POST'], 
    use_user=False  # Rate limit by IP instead of user
)
class PublicAPIView(APIView):
    def post(self, request):
        return Response({"message": "Public API response"})


if __name__ == "__main__":
    print("Rate limiting examples:")
    print("1. MyDjangoView - 100 requests per hour")
    print("2. SummarizeInputAIApiView - 50 POST requests per 30 minutes")
    print("3. CustomAPIView - 200 requests per hour with custom scope")
    print("4. PublicAPIView - 10 POST requests per minute (by IP)")
    print("\nThe fix ensures that 'request' parameter is correctly identified")
    print("even when decorating class methods where 'self' is the first parameter.")
