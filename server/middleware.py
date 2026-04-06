import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """Middleware for logging API requests and responses"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.async_mode = False
    
    def __call__(self, request):
        """Log incoming requests and responses"""
        request.start_time = time.time()
        
        # Log request details
        logger.info(f"Incoming request: {request.method} {request.path}")
        
        # Log user info if authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            logger.info(f"User: {request.user.email} (ID: {request.user.id})")
        
        response = self.get_response(request)
        
        # Log response details
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(f"Response: {response.status_code} ({duration:.3f}s)")
        
        return response


class SecurityHeadersMiddleware:
    """Middleware for adding security headers"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.async_mode = False
    
    def __call__(self, request):
        """Add security headers to response"""
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Add API specific headers for API requests
        if request.path.startswith('/api/'):
            response['Access-Control-Expose-Headers'] = 'Content-Type, Authorization'
        
        return response


class RateLimitMiddleware:
    """Simple rate limiting middleware"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}  # In production, use Redis or similar
        self.async_mode = False  # Add this attribute to fix the error
        
    def __call__(self, request):
        """Check rate limits"""
        if not request.path.startswith('/api/'):
            return self.get_response(request)
        
        # Get client IP
        client_ip = self.get_client_ip(request)
        
        # Simple rate limiting: 100 requests per minute per IP
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Clean old entries
        if client_ip in self.request_counts:
            self.request_counts[client_ip] = [
                req_time for req_time in self.request_counts[client_ip] 
                if req_time > minute_ago
            ]
        else:
            self.request_counts[client_ip] = []
        
        # Check rate limit
        if len(self.request_counts[client_ip]) >= 100:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JsonResponse({
                'error': 'Rate Limit Exceeded',
                'message': 'Too many requests. Please try again later.',
                'code': 'rate_limit_exceeded',
                'status': 'error'
            }, status=429)
        
        # Add current request
        self.request_counts[client_ip].append(current_time)
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ValidationMiddleware:
    """Middleware for basic request validation"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.async_mode = False
    
    def __call__(self, request):
        """Validate basic request parameters"""
        if not request.path.startswith('/api/'):
            return self.get_response(request)
        
        # Validate content type for POST/PUT/PATCH requests
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.content_type
            
            # For file uploads, allow multipart/form-data
            if 'upload' in request.path or 'file' in request.path:
                if content_type and not content_type.startswith('multipart/form-data'):
                    logger.warning(f"Invalid content type for file upload: {content_type}")
                    return JsonResponse({
                        'error': 'Invalid Content Type',
                        'message': 'File uploads must use multipart/form-data',
                        'code': 'invalid_content_type',
                        'status': 'error'
                    }, status=400)
            
            # For regular API requests, expect JSON
            elif content_type and not content_type.startswith('application/json'):
                logger.warning(f"Invalid content type for API request: {content_type}")
                return JsonResponse({
                    'error': 'Invalid Content Type',
                    'message': 'API requests must use application/json',
                    'code': 'invalid_content_type',
                    'status': 'error'
                }, status=400)
        
        return self.get_response(request)


class ErrorHandlingMiddleware:
    """Middleware for handling uncaught exceptions"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.async_mode = False
    
    def __call__(self, request):
        """Handle uncaught exceptions"""
        try:
            return self.get_response(request)
        except Exception as exception:
            # Only handle API requests
            if not request.path.startswith('/api/'):
                raise
            
            logger.error(f"Uncaught exception in API request: {str(exception)}")
            
            # Return consistent error response
            return JsonResponse({
                'error': 'Server Error',
                'message': 'An internal server error occurred',
                'code': 'server_error',
                'status': 'error'
            }, status=500)
