"""
Test utilities and fixtures for common test scenarios
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from auth_api.models import User, Employee
from admin_api.models import Batch, Lead, LeadBoardScore, LeadSaleStatus, LeadAccountStatus, LeadOperationStatus
from django.core.files.uploadedfile import SimpleUploadedFile
from test_utils import create_test_user, create_test_superuser

User = get_user_model()


class TestFixtureMixin:
    """Mixin providing common test fixtures and utilities"""
    
    @classmethod
    def setUpTestData(cls):
        # Create admin user with unique email
        cls.admin_user = create_test_superuser(
            email='admin@example.com',
            name='Admin User',
            contact='+1234567890',
            type='admin',
            password='adminpass123'
        )
        
        cls.sales_user = create_test_user(
            email='sales@example.com',
            name='Sales User',
            contact='+1234567891',
            type='sales',
            password='salespass123'
        )
        
        cls.ops_user = create_test_user(
            email='ops@example.com',
            name='Operations User',
            contact='+1234567892',
            type='operations',
            password='opspass123'
        )
        
        # Create employees
        cls.admin_employee = Employee.objects.create(
            user=cls.admin_user,
            type='admin',
            allot=100
        )
        
        cls.sales_employee = Employee.objects.create(
            user=cls.sales_user,
            type='sales',
            allot=50
        )
        
        # Create batches
        cls.active_batch = Batch.objects.create(
            name='Active-Batch-001',
            book_price=5000,
            price=15000,
            status='active'
        )
        
        cls.inactive_batch = Batch.objects.create(
            name='Inactive-Batch-002',
            book_price=6000,
            price=18000,
            status='inactive'
        )
        
        # Create leads with unique contact numbers
        cls.new_lead = Lead.objects.create(
            name='John Doe',
            contact_number='+12345678901',
            source='website',
            status='new'
        )
        
        cls.assigned_lead = Lead.objects.create(
            name='Jane Smith',
            contact_number='+12345678902',
            source='referral',
            status='contacted',
            assigned_to=cls.sales_user
        )
        
        cls.payment_received_lead = Lead.objects.create(
            name='Bob Johnson',
            contact_number='+12345678903',
            source='direct',
            status='payment_received',
            assigned_to=cls.sales_user
        )
        
        cls.interested_lead = Lead.objects.create(
            name='Alice Brown',
            contact_number='+12345678904',
            source='website',
            status='interested',
            assigned_to=cls.sales_user
        )
        
        # Create lead sale statuses
        cls.complete_sale_status = LeadSaleStatus.objects.create(
            lead=cls.payment_received_lead,
            batch=cls.active_batch,
            status='payment_received',
            form_ss=cls.create_test_image(),
            payment_ss=cls.create_test_image(),
            buy_books=True,
            books_ss=cls.create_test_image(),
            recieved_date=date.today()
        )
        
        cls.incomplete_sale_status = LeadSaleStatus.objects.create(
            lead=cls.interested_lead,
            batch=cls.active_batch,
            status='interested',
            form_ss=cls.create_test_image()
        )
        
        # Create lead account statuses
        cls.verified_account_status = LeadAccountStatus.objects.create(
            lead=cls.payment_received_lead,
            payment_verification_status='verified'
        )
        
        cls.unverified_account_status = LeadAccountStatus.objects.create(
            lead=cls.interested_lead,
            payment_verification_status='unverified'
        )
        
        # Create lead operation statuses
        cls.complete_operation_status = LeadOperationStatus.objects.create(
            lead=cls.payment_received_lead,
            added_to_group=True,
            registered_on_app=True
        )
        
        cls.incomplete_operation_status = LeadOperationStatus.objects.create(
            lead=cls.interested_lead,
            added_to_group=False,
            registered_on_app=False
        )
        
        # Create lead board scores
        cls.board_score = LeadBoardScore.objects.create(
            lead=cls.payment_received_lead,
            year='2024',
            english_score='85%',
            pcm_score='90%'
        )
    
    @staticmethod
    def create_test_image(name="test_image.jpg", content=b"file_content"):
        """Create a test image file for file upload tests"""
        return SimpleUploadedFile(
            name,
            content,
            content_type="image/jpeg"
        )
    
    @staticmethod
    def create_test_pdf(name="test_document.pdf", content=b"pdf_content"):
        """Create a test PDF file for document upload tests"""
        return SimpleUploadedFile(
            name,
            content,
            content_type="application/pdf"
        )
    
    def authenticate_as_admin(self):
        """Authenticate client as admin user"""
        self.client.force_authenticate(user=self.admin_user)
    
    def authenticate_as_sales(self):
        """Authenticate client as sales user"""
        self.client.force_authenticate(user=self.sales_user)
    
    def authenticate_as_ops(self):
        """Authenticate client as operations user"""
        self.client.force_authenticate(user=self.ops_user)
    
    def create_lead_with_full_workflow(self, name="Test Lead", contact="+1234567899"):
        """Create a lead with complete workflow setup"""
        lead = Lead.objects.create(
            name=name,
            contact_number=contact,
            source='website',
            status='new'
        )
        
        sale_status = LeadSaleStatus.objects.create(
            lead=lead,
            batch=self.active_batch,
            status='interested',
            comment='Initial interest'
        )
        
        account_status = LeadAccountStatus.objects.create(
            lead=lead,
            payment_verification_status='unverified'
        )
        
        operation_status = LeadOperationStatus.objects.create(
            lead=lead,
            added_to_group=False,
            registered_on_app=False
        )
        
        return lead, sale_status, account_status, operation_status
    
    def assertAPIResponse(self, response, expected_status=status.HTTP_200_OK, 
                         expected_fields=None, expected_count=None):
        """Utility method to assert common API response properties"""
        self.assertEqual(response.status_code, expected_status)
        
        if expected_fields:
            for field in expected_fields:
                self.assertIn(field, response.data)
        
        if expected_count is not None:
            if isinstance(response.data, list):
                self.assertEqual(len(response.data), expected_count)
            elif 'results' in response.data:
                self.assertEqual(len(response.data['results']), expected_count)
    
    def assertValidationError(self, response, field_name=None):
        """Utility method to assert validation error response"""
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        if field_name:
            self.assertIn(field_name, response.data)


class IntegrationTestCase(APITestCase):
    """Base class for integration tests with fixtures"""
    
    @staticmethod
    def create_test_image(name="test_image.jpg", content=b"file_content"):
        """Create a test image file for file upload tests"""
        return SimpleUploadedFile(
            name=name,
            content=content,
            content_type="image/jpeg"
        )
    
    def create_lead_with_full_workflow(self, name="Test Lead", contact="+1234567899"):
        """Create a lead with complete workflow setup"""
        lead = Lead.objects.create(
            name=name,
            contact_number=contact,
            source='website',
            status='new'
        )
        
        sale_status = LeadSaleStatus.objects.create(
            lead=lead,
            batch=self.active_batch,
            status='interested',
            comment='Initial interest'
        )
        
        account_status = LeadAccountStatus.objects.create(
            lead=lead,
            payment_verification_status='unverified'
        )
        
        operation_status = LeadOperationStatus.objects.create(
            lead=lead,
            added_to_group=False,
            registered_on_app=False
        )
        
        return lead, sale_status, account_status, operation_status
    
    @classmethod
    def setUpTestData(cls):
        import uuid
        suffix = str(uuid.uuid4())[:8]
        
        # Create admin user with unique email
        cls.admin_user = create_test_superuser(
            email='admin@example.com',
            name='Admin User',
            contact=f'+12345678901',
            type='admin',
            password='adminpass123'
        )
        
        cls.sales_user = create_test_user(
            email='sales@example.com',
            name='Sales User',
            contact=f'+12345678902',
            type='sales',
            password='salespass123'
        )
        
        cls.ops_user = create_test_user(
            email='ops@example.com',
            name='Operations User',
            contact=f'+12345678903',
            type='operations',
            password='opspass123'
        )
        
        # Create employees
        cls.admin_employee = Employee.objects.create(
            user=cls.admin_user,
            type='admin',
            allot=100
        )
        
        cls.sales_employee = Employee.objects.create(
            user=cls.sales_user,
            type='sales',
            allot=50
        )
        
        # Create batches
        cls.active_batch = Batch.objects.create(
            name='Active-Batch-001',
            book_price=5000,
            price=15000,
            status='active'
        )
        
        cls.inactive_batch = Batch.objects.create(
            name='Inactive-Batch-002',
            book_price=6000,
            price=18000,
            status='inactive'
        )
        
        # Create leads with unique contact numbers
        cls.new_lead = Lead.objects.create(
            name='John Doe',
            contact_number='+12345678910',
            source='website',
            status='new'
        )
        
        cls.assigned_lead = Lead.objects.create(
            name='Jane Smith',
            contact_number='+12345678911',
            source='referral',
            status='contacted',
            assigned_to=cls.sales_user
        )
        
        cls.payment_received_lead = Lead.objects.create(
            name='Bob Johnson',
            contact_number='+12345678912',
            source='direct',
            status='payment_received',
            assigned_to=cls.sales_user
        )
        
        cls.interested_lead = Lead.objects.create(
            name='Alice Brown',
            contact_number='+12345678913',
            source='website',
            status='interested',
            assigned_to=cls.sales_user
        )
        
        # Create lead sale statuses
        cls.complete_sale_status = LeadSaleStatus.objects.create(
            lead=cls.payment_received_lead,
            batch=cls.active_batch,
            status='payment_received',
            form_ss=cls.create_test_image(),
            payment_ss=cls.create_test_image(),
            buy_books=True,
            books_ss=cls.create_test_image(),
            recieved_date=date.today()
        )
        
        cls.incomplete_sale_status = LeadSaleStatus.objects.create(
            lead=cls.interested_lead,
            batch=cls.active_batch,
            status='interested',
            form_ss=cls.create_test_image()
        )
        
        # Create lead account statuses
        cls.verified_account_status = LeadAccountStatus.objects.create(
            lead=cls.payment_received_lead,
            payment_verification_status='verified'
        )
        
        cls.pending_account_status = LeadAccountStatus.objects.create(
            lead=cls.interested_lead,
            payment_verification_status='pending'
        )
        
        # Create lead operation statuses
        cls.group_added_status = LeadOperationStatus.objects.create(
            lead=cls.payment_received_lead,
            added_to_group=True
        )
        
        cls.app_registered_status = LeadOperationStatus.objects.create(
            lead=cls.payment_received_lead,
            registered_on_app=True
        )


class ModelTestCase(TestCase):
    """Base class for model tests with fixtures"""
    
    @staticmethod
    def create_test_image(name="test_image.jpg", content=b"file_content"):
        """Create a test image file for file upload tests"""
        return SimpleUploadedFile(
            name=name,
            content=content,
            content_type="image/jpeg"
        )
    
    def create_lead_with_full_workflow(self, name="Test Lead", contact="+1234567899"):
        """Create a lead with complete workflow setup"""
        lead = Lead.objects.create(
            name=name,
            contact_number=contact,
            source='website',
            status='new'
        )
        
        sale_status = LeadSaleStatus.objects.create(
            lead=lead,
            batch=self.active_batch,
            status='interested',
            comment='Initial interest'
        )
        
        account_status = LeadAccountStatus.objects.create(
            lead=lead,
            payment_verification_status='unverified'
        )
        
        operation_status = LeadOperationStatus.objects.create(
            lead=lead,
            added_to_group=False,
            registered_on_app=False
        )
        
        return lead, sale_status, account_status, operation_status
    
    @classmethod
    def setUpTestData(cls):
        import uuid
        suffix = str(uuid.uuid4())[:8]
        
        # Create admin user with unique email
        cls.admin_user = create_test_superuser(
            email='admin@example.com',
            name='Admin User',
            contact=f'+12345678801',
            type='admin',
            password='adminpass123'
        )
        
        cls.sales_user = create_test_user(
            email='sales@example.com',
            name='Sales User',
            contact=f'+12345678802',
            type='sales',
            password='salespass123'
        )
        
        cls.ops_user = create_test_user(
            email='ops@example.com',
            name='Operations User',
            contact=f'+12345678803',
            type='operations',
            password='opspass123'
        )
        
        # Create employees
        cls.admin_employee = Employee.objects.create(
            user=cls.admin_user,
            type='admin',
            allot=100
        )
        
        cls.sales_employee = Employee.objects.create(
            user=cls.sales_user,
            type='sales',
            allot=50
        )
        
        # Create batches
        cls.active_batch = Batch.objects.create(
            name='Active-Batch-001',
            book_price=5000,
            price=15000,
            status='active'
        )
        
        cls.inactive_batch = Batch.objects.create(
            name='Inactive-Batch-002',
            book_price=6000,
            price=18000,
            status='inactive'
        )
        
        # Create leads with unique contact numbers
        cls.new_lead = Lead.objects.create(
            name='John Doe',
            contact_number='+12345678810',
            source='website',
            status='new'
        )
        
        cls.assigned_lead = Lead.objects.create(
            name='Jane Smith',
            contact_number='+12345678811',
            source='referral',
            status='contacted',
            assigned_to=cls.sales_user
        )
        
        cls.payment_received_lead = Lead.objects.create(
            name='Bob Johnson',
            contact_number='+12345678812',
            source='direct',
            status='payment_received',
            assigned_to=cls.sales_user
        )
        
        cls.interested_lead = Lead.objects.create(
            name='Alice Brown',
            contact_number='+12345678813',
            source='website',
            status='interested',
            assigned_to=cls.sales_user
        )
        
        # Create lead sale statuses
        cls.complete_sale_status = LeadSaleStatus.objects.create(
            lead=cls.payment_received_lead,
            batch=cls.active_batch,
            status='payment_received',
            form_ss=cls.create_test_image(),
            payment_ss=cls.create_test_image(),
            buy_books=True,
            books_ss=cls.create_test_image(),
            recieved_date=date.today()
        )
        
        cls.incomplete_sale_status = LeadSaleStatus.objects.create(
            lead=cls.interested_lead,
            batch=cls.active_batch,
            status='interested',
            form_ss=cls.create_test_image()
        )
        
        # Create lead account statuses
        cls.verified_account_status = LeadAccountStatus.objects.create(
            lead=cls.payment_received_lead,
            payment_verification_status='verified'
        )
        
        cls.pending_account_status = LeadAccountStatus.objects.create(
            lead=cls.interested_lead,
            payment_verification_status='pending'
        )
        
        # Create lead operation statuses
        cls.group_added_status = LeadOperationStatus.objects.create(
            lead=cls.payment_received_lead,
            added_to_group=True
        )
        
        cls.app_registered_status = LeadOperationStatus.objects.create(
            lead=cls.payment_received_lead,
            registered_on_app=True
        )


class BusinessLogicTest(ModelTestCase):
    """Test cases for complex business logic"""
    
    def test_lead_status_validation_complete_workflow(self):
        """Test lead status validation through complete workflow"""
        # Start with interested lead
        lead, sale_status, account_status, operation_status = self.create_lead_with_full_workflow()
        
        # Initially should be False (incomplete workflow)
        self.assertFalse(lead.check_lead_update_status())
        
        # Add form screenshot
        sale_status.form_ss = self.create_test_image()
        sale_status.save()
        self.assertFalse(lead.check_lead_update_status())
        
        # Add payment screenshot
        sale_status.payment_ss = self.create_test_image()
        sale_status.save()
        self.assertTrue(lead.check_lead_update_status())  # Complete without books
        
        # Reset and test with books
        sale_status.form_ss = None
        sale_status.payment_ss = None
        sale_status.buy_books = True
        sale_status.save()
        self.assertFalse(lead.check_lead_update_status())
        
        # Add form, payment, and books screenshot
        sale_status.form_ss = self.create_test_image()
        sale_status.payment_ss = self.create_test_image()
        sale_status.books_ss = self.create_test_image()
        sale_status.save()
        self.assertTrue(lead.check_lead_update_status())  # Complete with books
    
    def test_lead_assignment_workflow(self):
        """Test lead assignment and workflow tracking"""
        # Create unassigned lead
        unassigned_lead = Lead.objects.create(
            name='Unassigned Lead',
            contact_number='+12345678905',
            source='website',
            status='new'
        )
        
        self.assertIsNone(unassigned_lead.assigned_to)
        
        # Assign to sales user
        unassigned_lead.assigned_to = self.sales_user
        unassigned_lead.save()
        
        self.assertEqual(unassigned_lead.assigned_to, self.sales_user)
        
        # Check that lead appears in user's assigned leads
        assigned_leads = Lead.objects.filter(assigned_to=self.sales_user)
        self.assertIn(unassigned_lead, assigned_leads)
    
    def test_batch_capacity_and_pricing(self):
        """Test batch management and pricing logic"""
        # Test batch pricing
        self.assertEqual(self.active_batch.price, 15000)
        self.assertEqual(self.active_batch.book_price, 5000)
        
        # Count existing leads in batch
        existing_count = LeadSaleStatus.objects.filter(batch=self.active_batch).count()
        
        # Create 3 additional leads for the batch
        leads_in_batch = []
        for i in range(3):
            lead, sale_status, _, _ = self.create_lead_with_full_workflow(
                name=f'Lead {chr(65+i)}',  # Lead A, Lead B, Lead C
                contact=f'+1234567890{i}'
            )
            sale_status.batch = self.active_batch
            sale_status.save()
            leads_in_batch.append(lead)
        
        # Check batch prospects
        batch_prospects = LeadSaleStatus.objects.filter(batch=self.active_batch)
        expected_count = existing_count + 3  # existing leads + 3 new leads
        self.assertEqual(batch_prospects.count(), expected_count)
    
    def test_user_role_permissions(self):
        """Test user role-based permissions"""
        # Admin should have admin privileges
        self.assertTrue(self.admin_user.is_admin)
        
        # Sales and ops users should not be admin
        self.assertFalse(self.sales_user.is_admin)
        self.assertFalse(self.ops_user.is_admin)
        
        # Check employee types
        self.assertEqual(self.admin_employee.type, 'admin')
        self.assertEqual(self.sales_employee.type, 'sales')
        
        # Check lead allotments
        self.assertEqual(self.admin_employee.allot, 100)
        self.assertEqual(self.sales_employee.allot, 50)


class PerformanceTest(ModelTestCase):
    """Test cases for performance and optimization"""
    
    def test_lead_query_performance(self):
        """Test lead query performance with filters"""
        import time
        
        # Create multiple leads for testing
        for i in range(20):
            Lead.objects.create(
                name=f'Lead {chr(65+i)}',  # Lead A, Lead B, etc.
                contact_number=f'+1234567890{i:02d}',
                source='website' if i % 2 == 0 else 'referral',
                status='new' if i % 3 == 0 else 'interested'
            )
        
        # Test query performance
        start_time = time.time()
        leads = Lead.objects.select_related('assigned_to').filter(
            status='new',
            source='website'
        )
        count = leads.count()
        end_time = time.time()
        
        # Query should complete quickly
        self.assertLess(end_time - start_time, 0.1)  # Less than 100ms
        self.assertGreater(count, 0)
    
    def test_batch_prospects_aggregation(self):
        """Test batch prospects aggregation performance"""
        import time
        
        # Create additional leads and sale statuses
        for i in range(10):
            lead = Lead.objects.create(
                name=f'Batch Lead {chr(65+i)}',  # Batch Lead A, Batch Lead B, etc.
                contact_number=f'+1234567880{i:02d}',
                source='website',
                status='interested'
            )
            LeadSaleStatus.objects.create(
                lead=lead,
                batch=self.active_batch,
                status='interested'
            )
        
        # Test aggregation query
        start_time = time.time()
        batch_stats = LeadSaleStatus.objects.filter(
            batch=self.active_batch
        ).values('status').annotate(count=models.Count('id'))
        end_time = time.time()
        
        # Query should complete quickly
        self.assertLess(end_time - start_time, 0.1)
        self.assertGreater(len(batch_stats), 0)


# Import models for aggregation test
from django.db import models
