from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from auth_api.models import User
from admin_api.models import Batch, Lead, LeadBoardScore, LeadSaleStatus, LeadAccountStatus, LeadOperationStatus
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class BatchModelTest(TestCase):
    """Test cases for Batch model"""

    def setUp(self):
        self.batch_data = {
            'name': 'Batch-2024-01',
            'book_price': 5000,
            'price': 15000,
            'status': 'active'
        }

    def test_create_batch(self):
        """Test creating a batch"""
        batch = Batch.objects.create(**self.batch_data)
        self.assertEqual(batch.name, self.batch_data['name'])
        self.assertEqual(batch.book_price, self.batch_data['book_price'])
        self.assertEqual(batch.price, self.batch_data['price'])
        self.assertEqual(batch.status, self.batch_data['status'])

    def test_batch_str_representation(self):
        """Test batch string representation - now has custom __str__"""
        batch = Batch.objects.create(**self.batch_data)
        self.assertEqual(str(batch), batch.name)


class LeadModelTest(TestCase):
    """Test cases for Lead model"""

    def setUp(self):
        # Create user using fixed UserManager
        self.user = User.objects.create_user(
            email='sales@example.com',
            name='Sales User',
            contact='+1234567890',
            type='sales',
            password='testpass123'
        )
        
        self.lead_data = {
            'name': 'John Doe',
            'contact_number': '+1234567890',
            'source': 'website',
            'status': 'new'
        }

    def test_create_lead(self):
        """Test creating a lead"""
        lead = Lead.objects.create(**self.lead_data)
        self.assertEqual(lead.name, self.lead_data['name'])
        self.assertEqual(lead.contact_number, self.lead_data['contact_number'])
        self.assertEqual(lead.source, self.lead_data['source'])
        self.assertEqual(lead.status, self.lead_data['status'])
        self.assertIsNone(lead.assigned_to)

    def test_create_lead_with_assignment(self):
        """Test creating a lead with user assignment"""
        lead = Lead.objects.create(assigned_to=self.user, **self.lead_data)
        self.assertEqual(lead.assigned_to, self.user)

    def test_lead_str_representation(self):
        """Test lead string representation - now has custom __str__"""
        lead = Lead.objects.create(**self.lead_data)
        self.assertEqual(str(lead), f"{lead.name} - {lead.contact_number}")

    def test_check_lead_update_status_complete_without_books(self):
        """Test lead status check without books purchased"""
        # Create lead
        lead = Lead.objects.create(**self.lead_data)
        
        # Create sale status with complete data (no books)
        sale_status = LeadSaleStatus.objects.create(
            lead=lead,
            batch=Batch.objects.create(name='Test Batch', book_price=5000, price=15000, status='active'),
            status='payment_received',
            form_ss=self._create_test_image(),
            payment_ss=self._create_test_image(),
            buy_books=False,
            recieved_date=date.today()
        )
        
        # Test the method on Lead model (not LeadSaleStatus)
        self.assertTrue(lead.check_lead_update_status())

    def test_check_lead_update_status_complete_with_books(self):
        """Test lead status check with books purchased"""
        # Create lead
        lead = Lead.objects.create(**self.lead_data)
        
        # Create sale status with complete data (with books)
        sale_status = LeadSaleStatus.objects.create(
            lead=lead,
            batch=Batch.objects.create(name='Test Batch', book_price=5000, price=15000, status='active'),
            status='payment_received',
            form_ss=self._create_test_image(),
            payment_ss=self._create_test_image(),
            buy_books=True,
            books_ss=self._create_test_image(),
            recieved_date=date.today()
        )
        
        # Test the method on Lead model (not LeadSaleStatus)
        self.assertTrue(lead.check_lead_update_status())

    def test_check_lead_update_status_incomplete_missing_payment(self):
        """Test lead status check with missing payment screenshot"""
        # Create lead
        lead = Lead.objects.create(**self.lead_data)
        
        # Create incomplete sale status
        sale_status = LeadSaleStatus.objects.create(
            lead=lead,
            batch=Batch.objects.create(name='Test Batch', book_price=5000, price=15000, status='active'),
            status='interested',
            form_ss=self._create_test_image(),
            buy_books=False
        )
        
        # Test the method on Lead model (not LeadSaleStatus)
        self.assertFalse(lead.check_lead_update_status())

    def test_check_lead_update_status_incomplete_missing_books_screenshot(self):
        """Test lead status check with books purchased but no screenshot"""
        # Create lead
        lead = Lead.objects.create(**self.lead_data)
        
        # Create incomplete sale status (books bought but no screenshot)
        sale_status = LeadSaleStatus.objects.create(
            lead=lead,
            batch=Batch.objects.create(name='Test Batch', book_price=5000, price=15000, status='active'),
            status='payment_received',
            form_ss=self._create_test_image(),
            payment_ss=self._create_test_image(),
            buy_books=True,
            recieved_date=date.today()
        )
        
        # Test the method on Lead model (not LeadSaleStatus)
        self.assertFalse(lead.check_lead_update_status())

    def _create_test_image(self):
        """Create a test image file"""
        return SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )


class LeadSaleStatusModelTest(TestCase):
    """Test cases for LeadSaleStatus model"""

    def setUp(self):
        self.lead = Lead.objects.create(
            name='John Doe',
            contact_number='+1234567890',
            source='website',
            status='new'
        )
        self.batch = Batch.objects.create(
            name='Batch-2024-01',
            book_price=5000,
            price=15000,
            status='active'
        )

    def test_create_lead_sale_status(self):
        """Test creating lead sale status"""
        sale_status = LeadSaleStatus.objects.create(
            lead=self.lead,
            batch=self.batch,
            status='interested',
            comment='Interested in course',
            followUpDate='2024-01-15'
        )
        self.assertEqual(sale_status.lead, self.lead)
        self.assertEqual(sale_status.batch, self.batch)
        self.assertEqual(sale_status.status, 'interested')
        self.assertEqual(sale_status.comment, 'Interested in course')

    def test_lead_sale_status_str_representation(self):
        """Test lead sale status string representation"""
        sale_status = LeadSaleStatus.objects.create(
            lead=self.lead,
            batch=self.batch,
            status='interested'
        )
        expected = "Lead Sale Details: batch: Batch-2024-01, recieved_date: None status: interested, comment: None, discount: False, discount_ss: None, buy_books: False, books_ss: None, form_ss: None created_at:"
        self.assertIn("Lead Sale Details:", str(sale_status))
        self.assertIn("batch: Batch-2024-01", str(sale_status))


class LeadAccountStatusModelTest(TestCase):
    """Test cases for LeadAccountStatus model"""

    def setUp(self):
        self.lead = Lead.objects.create(
            name='John Doe',
            contact_number='+1234567890',
            source='website',
            status='new'
        )

    def test_create_lead_account_status(self):
        """Test creating lead account status"""
        account_status = LeadAccountStatus.objects.create(
            lead=self.lead,
            payment_verification_status='verified'
        )
        self.assertEqual(account_status.lead, self.lead)
        self.assertEqual(account_status.payment_verification_status, 'verified')

    def test_lead_account_status_str_representation(self):
        """Test lead account status string representation"""
        account_status = LeadAccountStatus.objects.create(
            lead=self.lead,
            payment_verification_status='verified'
        )
        expected = f"Lead Account Details: payment_verification_status: verified"
        self.assertIn(expected, str(account_status))


class LeadOperationStatusModelTest(TestCase):
    """Test cases for LeadOperationStatus model"""

    def setUp(self):
        self.lead = Lead.objects.create(
            name='John Doe',
            contact_number='+1234567890',
            source='website',
            status='new'
        )

    def test_create_lead_operation_status(self):
        """Test creating lead operation status"""
        operation_status = LeadOperationStatus.objects.create(
            lead=self.lead,
            added_to_group=True,
            registered_on_app=True
        )
        self.assertEqual(operation_status.lead, self.lead)
        self.assertTrue(operation_status.added_to_group)
        self.assertTrue(operation_status.registered_on_app)

    def test_lead_operation_status_str_representation(self):
        """Test lead operation status string representation"""
        operation_status = LeadOperationStatus.objects.create(
            lead=self.lead,
            added_to_group=True,
            registered_on_app=False
        )
        expected = f"Lead Operation Details: addedToGroup: True, registeredOnGroup: False"
        self.assertIn(expected, str(operation_status))


class LeadBoardScoreModelTest(TestCase):
    """Test cases for LeadBoardScore model"""

    def setUp(self):
        self.lead = Lead.objects.create(
            name='John Doe',
            contact_number='+1234567890',
            source='website',
            status='new'
        )

    def test_create_lead_board_score(self):
        """Test creating lead board score"""
        board_score = LeadBoardScore.objects.create(
            lead=self.lead,
            year='2024',
            english_score='85%',
            pcm_score='90%'
        )
        self.assertEqual(board_score.lead, self.lead)
        self.assertEqual(board_score.year, '2024')
        self.assertEqual(board_score.english_score, '85%')
        self.assertEqual(board_score.pcm_score, '90%')
