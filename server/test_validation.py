"""
Test script to verify input validation and error handling
Run with: python server/manage.py shell < test_validation.py
"""

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from validators import validate_email_format, validate_phone_number, validate_name
from exceptions import APIError, BusinessLogicError
from serializers import UserCreateSerializer, BatchCreateSerializer
from admin_api.models import Lead, Batch

User = get_user_model()


def test_email_validation():
    """Test email validation"""
    print("Testing email validation...")
    
    # Valid emails
    try:
        validate_email_format("test@example.com")
        print("✅ Valid email: test@example.com")
    except ValidationError:
        print("❌ Should be valid: test@example.com")
    
    try:
        validate_email_format("user.name+tag@domain.co.uk")
        print("✅ Valid email: user.name+tag@domain.co.uk")
    except ValidationError:
        print("❌ Should be valid: user.name+tag@domain.co.uk")
    
    # Invalid emails
    try:
        validate_email_format("invalid-email")
        print("❌ Should be invalid: invalid-email")
    except ValidationError:
        print("✅ Correctly rejected: invalid-email")
    
    try:
        validate_email_format("@domain.com")
        print("❌ Should be invalid: @domain.com")
    except ValidationError:
        print("✅ Correctly rejected: @domain.com")


def test_phone_validation():
    """Test phone number validation"""
    print("\nTesting phone validation...")
    
    # Valid phone numbers
    try:
        validate_phone_number("+1234567890")
        print("✅ Valid phone: +1234567890")
    except ValidationError:
        print("❌ Should be valid: +1234567890")
    
    try:
        validate_phone_number("+1 (234) 567-890")
        print("✅ Valid phone: +1 (234) 567-890")
    except ValidationError:
        print("❌ Should be valid: +1 (234) 567-890")
    
    # Invalid phone numbers
    try:
        validate_phone_number("123")
        print("❌ Should be invalid: 123")
    except ValidationError:
        print("✅ Correctly rejected: 123")
    
    try:
        validate_phone_number("abc123")
        print("❌ Should be invalid: abc123")
    except ValidationError:
        print("✅ Correctly rejected: abc123")


def test_name_validation():
    """Test name validation"""
    print("\nTesting name validation...")
    
    # Valid names
    try:
        validate_name("John Doe")
        print("✅ Valid name: John Doe")
    except ValidationError:
        print("❌ Should be valid: John Doe")
    
    try:
        validate_name("Mary-Jane O'Connor")
        print("✅ Valid name: Mary-Jane O'Connor")
    except ValidationError:
        print("❌ Should be valid: Mary-Jane O'Connor")
    
    # Invalid names
    try:
        validate_name("")
        print("❌ Should be invalid: empty string")
    except ValidationError:
        print("✅ Correctly rejected: empty string")
    
    try:
        validate_name("John123")
        print("❌ Should be invalid: John123")
    except ValidationError:
        print("✅ Correctly rejected: John123")


def test_user_serializer_validation():
    """Test user serializer validation"""
    print("\nTesting user serializer validation...")
    
    # Valid user data
    valid_data = {
        'email': 'test@example.com',
        'name': 'John Doe',
        'contact': '+1234567890',
        'type': 'sales',
        'password': 'SecurePass123',
        'confirm_password': 'SecurePass123'
    }
    
    serializer = UserCreateSerializer(data=valid_data)
    if serializer.is_valid():
        print("✅ Valid user data passed validation")
    else:
        print(f"❌ Valid user data failed: {serializer.errors}")
    
    # Invalid email
    invalid_data = valid_data.copy()
    invalid_data['email'] = 'invalid-email'
    
    serializer = UserCreateSerializer(data=invalid_data)
    if not serializer.is_valid():
        print("✅ Invalid email correctly rejected")
    else:
        print("❌ Invalid email was accepted")
    
    # Weak password
    invalid_data = valid_data.copy()
    invalid_data['password'] = 'weak'
    invalid_data['confirm_password'] = 'weak'
    
    serializer = UserCreateSerializer(data=invalid_data)
    if not serializer.is_valid():
        print("✅ Weak password correctly rejected")
    else:
        print("❌ Weak password was accepted")


def test_batch_serializer_validation():
    """Test batch serializer validation"""
    print("\nTesting batch serializer validation...")
    
    # Valid batch data
    valid_data = {
        'name': 'Batch-2024-01',
        'book_price': 5000,
        'price': 15000,
        'status': 'active'
    }
    
    serializer = BatchCreateSerializer(data=valid_data)
    if serializer.is_valid():
        print("✅ Valid batch data passed validation")
    else:
        print(f"❌ Valid batch data failed: {serializer.errors}")
    
    # Price less than book price
    invalid_data = valid_data.copy()
    invalid_data['price'] = 3000  # Less than book_price
    
    serializer = BatchCreateSerializer(data=invalid_data)
    if not serializer.is_valid():
        print("✅ Invalid price relationship correctly rejected")
    else:
        print("❌ Invalid price relationship was accepted")


def test_model_validation():
    """Test model-level validation"""
    print("\nTesting model validation...")
    
    # Test batch validation
    try:
        batch = Batch(
            name='Test Batch',
            book_price=5000,
            price=3000,  # Invalid: less than book_price
            status='active'
        )
        batch.full_clean()
        print("❌ Invalid batch was accepted")
    except ValidationError:
        print("✅ Invalid batch correctly rejected")
    
    # Test lead validation
    try:
        from auth_api.models import User
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            contact='+1234567890',
            type='sales',
            password='testpass123'
        )
        
        lead = Lead(
            name='Test Lead',
            contact_number='+1234567891',
            source='website',
            status='new',
            assigned_to=user
        )
        lead.full_clean()
        print("✅ Valid lead passed validation")
    except ValidationError as e:
        print(f"❌ Valid lead failed validation: {e}")


def test_custom_exceptions():
    """Test custom exception classes"""
    print("\nTesting custom exceptions...")
    
    try:
        raise APIError("Test API error")
    except APIError as e:
        print(f"✅ APIError caught: {e}")
    
    try:
        raise BusinessLogicError("Test business logic error")
    except BusinessLogicError as e:
        print(f"✅ BusinessLogicError caught: {e}")


def run_all_tests():
    """Run all validation tests"""
    print("=" * 50)
    print("INPUT VALIDATION AND ERROR HANDLING TESTS")
    print("=" * 50)
    
    test_email_validation()
    test_phone_validation()
    test_name_validation()
    test_user_serializer_validation()
    test_batch_serializer_validation()
    test_model_validation()
    test_custom_exceptions()
    
    print("\n" + "=" * 50)
    print("TESTS COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
