from django.db import models
from django.core.exceptions import ValidationError
from auth_api.models import User
from validators import validate_name, validate_phone_number, validate_lead_status, validate_batch_name, validate_price, validate_batch_status


class Batch(models.Model):
    name = models.CharField(
        max_length=50,  # Increased for better naming
        error_messages={
            'max_length': 'Batch name cannot be longer than 50 characters.',
        }
    )
    book_price = models.IntegerField(
        error_messages={
            'invalid': 'Book price must be a valid number.',
        }
    )
    status = models.CharField(
        max_length=20,  # Increased for more status options
        default="active",
        error_messages={
            'max_length': 'Status cannot be longer than 20 characters.',
        }
    )
    price = models.IntegerField(
        error_messages={
            'invalid': 'Price must be a valid number.',
        }
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    
    def clean(self):
        """Custom validation for batch fields"""
        super().clean()
        validate_batch_name(self.name)
        validate_price(self.book_price)
        validate_price(self.price)
        validate_batch_status(self.status)
        
        # Business logic validation
        if self.price < self.book_price:
            raise ValidationError('Total price cannot be less than book price.')
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation before saving
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name     
    
    
class Lead(models.Model):
    assigned_to = models.ForeignKey(
        User, 
        related_name="assigned_leads", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        error_messages={
            'invalid': 'Please select a valid user.',
        }
    )
    name = models.CharField(
        max_length=72,
        error_messages={
            'max_length': 'Name cannot be longer than 72 characters.',
        }
    )
    contact_number = models.CharField(
        max_length=20,  # Increased for international numbers
        unique=True,
        error_messages={
            'max_length': 'Contact number cannot be longer than 20 characters.',
            'unique': 'A lead with this contact number already exists.',
        }
    )
    source = models.CharField(
        max_length=20,  # Increased for more source options
        default="direct",
        error_messages={
            'max_length': 'Source cannot be longer than 20 characters.',
        }
    )
    status = models.CharField(
        max_length=20,  # Increased for more status options
        default="new",
        error_messages={
            'max_length': 'Status cannot be longer than 20 characters.',
        }
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    
    def clean(self):
        """Custom validation for lead fields"""
        super().clean()
        validate_name(self.name)
        validate_phone_number(self.contact_number)
        validate_lead_status(self.status)
        
        # Business logic validation
        if self.assigned_to and self.assigned_to.type != 'sales':
            raise ValidationError('Leads can only be assigned to sales users.')
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation before saving
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.contact_number}"
    
    def check_lead_update_status(self):
        sale_details = self.sale_details.first()
        if not sale_details:
            return False
            
        if (sale_details.form_ss) and  (sale_details.payment_ss):    
            if (sale_details.buy_books):
                if (sale_details.books_ss):
                    if (sale_details.discount):
                        if (sale_details.discount_ss):
                            return True
                        else: 
                            return False
                    else:
                        return True  # If books bought, books_ss present, and no discount, return True
                else:
                    return False
            else:
                if (sale_details.discount):
                    if (sale_details.discount_ss):
                        return True
                    else: 
                        return False
                else:
                    return True   
        return False
                    
        
    
class LeadBoardScore(models.Model):
    lead = models.ForeignKey(Lead, related_name="board_score", on_delete=models.CASCADE)
    year = models.CharField(max_length=4, blank=True, null=True)
    english_score = models.CharField(max_length=20, blank=True, null=True)
    pcm_score = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    
class LeadSaleStatus(models.Model):
    lead = models.ForeignKey(Lead, related_name="sale_details", on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, related_name="prospects", on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, default="interested")
    comment = models.TextField(blank=True, null=True) 
    followUpDate = models.CharField(blank=True, null=True, max_length=30)
    form_ss = models.ImageField(upload_to="images/", null=True, blank=True)
    discount = models.BooleanField(default=False)
    discount_ss = models.ImageField(upload_to="images/", null=True, blank=True)
    buy_books = models.BooleanField(default=False)
    books_ss = models.ImageField(upload_to="images/", null=True, blank=True)
    payment_ss = models.ImageField(upload_to="images/", blank=True, null=True)
    recieved_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return f"Lead Sale Details: batch: {self.batch}, recieved_date: {self.recieved_date} status: {self.status}, comment: {self.comment}, discount: {self.discount}, discount_ss: {self.discount_ss}, buy_books: {self.buy_books}, books_ss: {self.books_ss}, form_ss: {self.form_ss} created_at: {self.created_at}, updated_at: {self.updated_at}"
    
    
class LeadAccountStatus(models.Model):
    lead = models.ForeignKey(Lead, related_name="account_details", on_delete=models.CASCADE)
    payment_verification_status = models.CharField(default="unverified", max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    
    def __str__(self):
        return f"Lead Account Details: payment_verification_status: {self.payment_verification_status}, created_at: {self.created_at}, updated_at: {self.updated_at}"

    
class LeadOperationStatus(models.Model):
    lead = models.ForeignKey(Lead, related_name="operations_details", on_delete=models.CASCADE)
    added_to_group = models.BooleanField(default=False)
    registered_on_app = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    
    def __str__(self):
        return f"Lead Operation Details: addedToGroup: {self.added_to_group}, registeredOnGroup: {self.registered_on_app}, created_at: {self.created_at}, updated_at: {self.updated_at}"
