import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value):
    """
    Validate phone number format
    Accepts formats: +1234567890, +1 234 567 890, (123) 456-7890
    """
    pattern = r'^[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Invalid phone number format. Please use a valid international format.')
        )


def validate_email_format(value):
    """
    Enhanced email validation
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        raise ValidationError(_('Invalid email format.'))
    
    # Check for common invalid patterns
    if '..' in value or value.startswith('.') or value.endswith('.'):
        raise ValidationError(_('Invalid email format.'))
    
    # Check domain
    domain = value.split('@')[1]
    if len(domain) < 2 or '.' not in domain:
        raise ValidationError(_('Invalid email domain.'))


def validate_name(value):
    """
    Validate name field - only letters, spaces, hyphens, and apostrophes
    """
    if not value or len(value.strip()) < 2:
        raise ValidationError(_('Name must be at least 2 characters long.'))
    
    if len(value) > 100:
        raise ValidationError(_('Name cannot be longer than 100 characters.'))
    
    pattern = r'^[a-zA-Z\s\-\'\.]+$'
    if not re.match(pattern, value):
        raise ValidationError(_('Name can only contain letters, spaces, hyphens, and apostrophes.'))


def validate_batch_name(value):
    """
    Validate batch name format
    """
    if not value or len(value.strip()) < 3:
        raise ValidationError(_('Batch name must be at least 3 characters long.'))
    
    if len(value) > 50:
        raise ValidationError(_('Batch name cannot be longer than 50 characters.'))
    
    # Allow alphanumeric, spaces, hyphens, underscores
    pattern = r'^[a-zA-Z0-9\s\-_]+$'
    if not re.match(pattern, value):
        raise ValidationError(_('Batch name can only contain letters, numbers, spaces, hyphens, and underscores.'))


def validate_price(value):
    """
    Validate price field - must be positive
    """
    if value <= 0:
        raise ValidationError(_('Price must be a positive value.'))
    
    if value > 999999.99:
        raise ValidationError(_('Price cannot exceed 999,999.99.'))


def validate_lead_status(value):
    """
    Validate lead status
    """
    valid_statuses = [
        'new', 'contacted', 'interested', 'not_interested', 
        'payment_received', 'payment_pending', 'closed-success', 
        'closed-failed', 'dnp'
    ]
    
    if value not in valid_statuses:
        raise ValidationError(
            _('Invalid status. Must be one of: %(statuses)s') % 
            {'statuses': ', '.join(valid_statuses)}
        )


def validate_batch_status(value):
    """
    Validate batch status
    """
    valid_statuses = ['active', 'inactive', 'completed', 'upcoming']
    
    if value not in valid_statuses:
        raise ValidationError(
            _('Invalid batch status. Must be one of: %(statuses)s') % 
            {'statuses': ', '.join(valid_statuses)}
        )


def validate_file_size(value, max_size_mb=5):
    """
    Validate file size
    """
    max_size = max_size_mb * 1024 * 1024  # Convert to bytes
    if value.size > max_size:
        raise ValidationError(
            _('File size cannot exceed %(max_size)d MB.') % 
            {'max_size': max_size_mb}
        )


def validate_file_type(value, allowed_types):
    """
    Validate file type
    """
    file_extension = value.name.split('.')[-1].lower()
    if file_extension not in allowed_types:
        raise ValidationError(
            _('Invalid file type. Allowed types: %(types)s') % 
            {'types': ', '.join(allowed_types)}
        )


def validate_image_file(value):
    """
    Validate uploaded image files
    """
    allowed_types = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
    validate_file_size(value, max_size_mb=5)
    validate_file_type(value, allowed_types)


def validate_excel_file(value):
    """
    Validate uploaded Excel files
    """
    allowed_types = ['xlsx', 'xls', 'csv']
    validate_file_size(value, max_size_mb=10)
    validate_file_type(value, allowed_types)


def validate_user_type(value):
    """
    Validate user type
    """
    valid_types = ['admin', 'sales', 'operations']
    
    if value not in valid_types:
        raise ValidationError(
            _('Invalid user type. Must be one of: %(types)s') % 
            {'types': ', '.join(valid_types)}
        )


def validate_contact_number_uniqueness(value, user_id=None):
    """
    Validate contact number uniqueness (excluding current user)
    """
    from auth_api.models import User
    
    queryset = User.objects.filter(contact=value)
    if user_id:
        queryset = queryset.exclude(id=user_id)
    
    if queryset.exists():
        raise ValidationError(_('This contact number is already registered.'))


def validate_email_uniqueness(value, user_id=None):
    """
    Validate email uniqueness (excluding current user)
    """
    from auth_api.models import User
    
    queryset = User.objects.filter(email=value)
    if user_id:
        queryset = queryset.exclude(id=user_id)
    
    if queryset.exists():
        raise ValidationError(_('This email address is already registered.'))
