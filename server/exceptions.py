from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotAuthenticated
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Global exception handler for consistent error responses
    """
    # Default response
    response = exception_handler(exc, context)
    
    # Log the error
    logger.error(f"Exception: {exc} - Context: {context}")
    
    # Handle different exception types
    if isinstance(exc, ValidationError):
        # Django validation errors
        return Response({
            'error': 'Validation Error',
            'message': str(exc),
            'code': 'validation_error',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, AuthenticationFailed):
        # Authentication errors
        return Response({
            'error': 'Authentication Failed',
            'message': 'Invalid authentication credentials',
            'code': 'authentication_error',
            'status': 'error'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    elif isinstance(exc, NotAuthenticated):
        # Not authenticated
        return Response({
            'error': 'Authentication Required',
            'message': 'Authentication credentials were not provided',
            'code': 'not_authenticated',
            'status': 'error'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    elif isinstance(exc, PermissionDenied):
        # Permission errors
        return Response({
            'error': 'Permission Denied',
            'message': 'You do not have permission to perform this action',
            'code': 'permission_denied',
            'status': 'error'
        }, status=status.HTTP_403_FORBIDDEN)
    
    elif isinstance(exc, Http404):
        # Not found errors
        return Response({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'code': 'not_found',
            'status': 'error'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Handle DRF response errors
    if response is not None:
        # Customize DRF error responses
        if response.status_code == 400:
            response.data = {
                'error': 'Bad Request',
                'message': response.data,
                'code': 'bad_request',
                'status': 'error'
            }
        elif response.status_code == 401:
            response.data = {
                'error': 'Unauthorized',
                'message': 'Authentication credentials were not provided',
                'code': 'unauthorized',
                'status': 'error'
            }
        elif response.status_code == 403:
            response.data = {
                'error': 'Forbidden',
                'message': 'You do not have permission to perform this action',
                'code': 'forbidden',
                'status': 'error'
            }
        elif response.status_code == 404:
            response.data = {
                'error': 'Not Found',
                'message': 'The requested resource was not found',
                'code': 'not_found',
                'status': 'error'
            }
        elif response.status_code == 405:
            response.data = {
                'error': 'Method Not Allowed',
                'message': 'The request method is not allowed for this endpoint',
                'code': 'method_not_allowed',
                'status': 'error'
            }
        elif response.status_code >= 500:
            response.data = {
                'error': 'Server Error',
                'message': 'An internal server error occurred',
                'code': 'server_error',
                'status': 'error'
            }
    
    return response


class APIError(Exception):
    """Custom API error class"""
    def __init__(self, message, code='api_error', status_code=400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class BusinessLogicError(APIError):
    """Business logic validation error"""
    def __init__(self, message):
        super().__init__(message, 'business_logic_error', 400)


class DataIntegrityError(APIError):
    """Data integrity error"""
    def __init__(self, message):
        super().__init__(message, 'data_integrity_error', 400)
