from django.test import TestCase
from django.contrib.auth import get_user_model
from auth_api.models import User, Employee
from test_utils import create_test_user, create_test_superuser

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for User model"""

    def test_create_user(self):
        """Test creating a regular user"""
        user = create_test_user(
            email='test@example.com',
            name='Test User',
            contact='+1234567890',
            type='sales',
            password='testpass123'
        )
        self.assertEqual(user.email, user._actual_email)  # Use actual email
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.contact, '+1234567890')
        self.assertEqual(user.type, 'sales')
        self.assertFalse(user.is_admin)
        self.assertTrue(user.check_password('testpass123'))

    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = create_test_superuser(
            email='admin@example.com',
            name='Admin User',
            contact='+1234567890',
            type='admin',
            password='adminpass123'
        )
        self.assertEqual(superuser.email, superuser._actual_email)  # Use actual email
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_str_representation(self):
        """Test user string representation"""
        user = create_test_user(
            email='test@example.com',
            name='Test User',
            contact='+1234567890',
            type='sales',
            password='testpass123'
        )
        expected = f"User Details: name: Test User, email: {user.email}, admin: False, contact: +1234567890"
        self.assertEqual(str(user), expected)

    def test_user_natural_key(self):
        """Test user natural key by email"""
        user = create_test_user(
            email='test@example.com',
            name='Test User',
            contact='+1234567890',
            type='sales',
            password='testpass123'
        )
        natural_user = User.objects.get_by_natural_key(user.email)
        self.assertEqual(user, natural_user)


class EmployeeModelTest(TestCase):
    """Test cases for Employee model"""

    def setUp(self):
        self.user = create_test_user(
            email='employee@example.com',
            name='Employee User',
            contact='+1234567890',
            type='sales',
            password='testpass123'
        )

    def test_create_employee(self):
        """Test creating an employee"""
        employee = Employee.objects.create(
            user=self.user,
            type='sales',
            allot=50
        )
        self.assertEqual(employee.user, self.user)
        self.assertEqual(employee.type, 'sales')
        self.assertEqual(employee.allot, 50)

    def test_employee_str_representation(self):
        """Test employee string representation"""
        employee = Employee.objects.create(
            user=self.user,
            type='sales',
            allot=50
        )
        expected = f"Emp Details: name: {self.user.name}, email: {self.user.email}, admin: {self.user.is_admin}, contact: {self.user.contact}, alloted_leads: 50, employee type: sales"
        self.assertEqual(str(employee), expected)


class EmailBackendTest(TestCase):
    """Test cases for custom email authentication backend"""

    def setUp(self):
        self.user = create_test_user(
            email='test@example.com',
            name='Test User',
            contact='+1234567890',
            type='sales',
            password='testpass123'
        )

    def test_email_backend_authentication(self):
        """Test email backend authentication"""
        from auth_api.backends import EmailBackend
        
        backend = EmailBackend()
        authenticated_user = backend.authenticate(
            request=None,
            email=self.user.email,  # Use the actual email created
            password='testpass123'
        )
        self.assertEqual(authenticated_user, self.user)

    def test_email_backend_invalid_password(self):
        """Test email backend with invalid password"""
        from auth_api.backends import EmailBackend
        
        backend = EmailBackend()
        authenticated_user = backend.authenticate(
            request=None,
            email='test@example.com',
            password='wrongpassword'
        )
        self.assertIsNone(authenticated_user)

    def test_email_backend_nonexistent_user(self):
        """Test email backend with non-existent user"""
        from auth_api.backends import EmailBackend
        
        backend = EmailBackend()
        authenticated_user = backend.authenticate(
            request=None,
            email='nonexistent@example.com',
            password='testpass123'
        )
        self.assertIsNone(authenticated_user)
