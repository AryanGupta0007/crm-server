from django.contrib.auth.backends import ModelBackend
from .models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
import jwt
from server.settings import SECRET_KEY

User = get_user_model()
class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # No auth header → DRF will continue checking other authenticators

        # Skip prefix validation — assume entire value is the token
        token = auth_header.strip()

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])  # adjust as per your settings
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)
