import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware for logging API requests and responses"""
    
    def process_request(self, request):
        """Log incoming requests"""
        request.start_time = time.time()
        
        # Log request details
        logger.info(f"Incoming request: {request.method} {request.path}")
        
        # Log user info if authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            logger.info(f"User: {request.user.email} (ID: {request.user.id})")
        
        return None
    
    def process_response(self, request, response):
        """Log outgoing responses"""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(f"Response: {response.status_code} - Duration: {duration:.2f}s")
        
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Middleware for adding security headers"""
    
    def process_response(self, request, response):
        """Add security headers to response"""
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Add API specific headers for API requests
        if request.path.startswith('/api/'):
            response['Access-Control-Expose-Headers'] = 'Content-Type, Authorization'
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """Simple rate limiting middleware"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}  # In production, use Redis or similar
        
    def process_request(self, request):
        """Check rate limits"""
        if not request.path.startswith('/api/'):
            return None
        
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
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ValidationMiddleware(MiddlewareMixin):
    """Middleware for basic request validation"""
    
    def process_request(self, request):
        """Validate basic request parameters"""
        if not request.path.startswith('/api/'):
            return None
        
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
                if not content_type.startswith('multipart/form-data'):
                    logger.warning(f"Invalid content type for API request: {content_type}")
                    return JsonResponse({
                        'error': 'Invalid Content Type',
                        'message': 'API requests must use application/json or multipart/form-data',
                        'code': 'invalid_content_type',
                        'status': 'error'
                    }, status=400)
        
        return None


class ErrorHandlingMiddleware(MiddlewareMixin):
    """Middleware for handling uncaught exceptions"""
    
    def process_exception(self, request, exception):
        """Handle uncaught exceptions"""
        # Only handle API requests
        if not request.path.startswith('/api/'):
            return None
        
        # Log the exception
        logger.error(f"Uncaught exception in {request.path}: {exception}", exc_info=True)
        
        # Return appropriate error response
        if isinstance(exception, ValidationError):
            return JsonResponse({
                'error': 'Validation Error',
                'message': str(exception),
                'code': 'validation_error',
                'status': 'error'
            }, status=400)
        
        elif isinstance(exception, APIException):
            return JsonResponse({
                'error': 'API Error',
                'message': str(exception),
                'code': 'api_error',
                'status': 'error'
            }, status=getattr(exception, 'status_code', 500))
        
        else:
            # Generic server error
            return JsonResponse({
                'error': 'Server Error',
                'message': 'An internal server error occurred',
                'code': 'server_error',
                'status': 'error'
            }, status=500)
