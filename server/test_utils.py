import uuid
from django.contrib.auth import get_user_model
from auth_api.models import User

User = get_user_model()


def create_test_user(email_suffix=None, **kwargs):
    """Create a test user with unique email to avoid constraint violations"""
    if email_suffix is None:
        email_suffix = str(uuid.uuid4())[:8]
    
    original_email = kwargs.get('email', 'test@example.com')
    base_email = original_email
    if '@' in base_email:
        email = base_email.replace('@', f'+{email_suffix}@')
    else:
        email = f'test{email_suffix}@example.com'
    
    user = User.objects.create_user(
        email=email,
        name=kwargs.get('name', 'Test User'),
        contact=kwargs.get('contact', '+12345678902'),
        type=kwargs.get('type', 'sales'),
        password=kwargs.get('password', 'testpass123')
    )
    
    # Store the original expected email for testing
    user._original_email = original_email
    user._actual_email = email
    return user


def create_test_superuser(email_suffix=None, **kwargs):
    """Create a test superuser with unique email"""
    if email_suffix is None:
        email_suffix = str(uuid.uuid4())[:8]
    
    original_email = kwargs.get('email', 'admin@example.com')
    base_email = original_email
    if '@' in base_email:
        email = base_email.replace('@', f'+{email_suffix}@')
    else:
        email = f'admin{email_suffix}@example.com'
    
    user = User.objects.create_user(
        email=email,
        name=kwargs.get('name', 'Admin User'),
        contact=kwargs.get('contact', '+12345678901'),
        type=kwargs.get('type', 'admin'),
        password=kwargs.get('password', 'adminpass123')
    )
    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save()
    
    # Store the original expected email for testing
    user._original_email = original_email
    user._actual_email = email
    return user
