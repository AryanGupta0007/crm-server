from django.db import models
from auth_api.models import User


class Batch(models.Model):
    name = models.CharField(max_length=20)
    book_price = models.IntegerField()
    status = models.CharField(max_length=10)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    
    
class Lead(models.Model):
    assigned_to = models.ForeignKey(User, related_name="assigned_leads", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=72)
    contact_number = models.CharField(max_length=72, unique=True)
    source = models.CharField(max_length=10, default="direct")
    status = models.CharField(max_length=20, default="new")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    
class LeadAccountStatus(models.Model):
    lead = models.ForeignKey(Lead, related_name="account_details", on_delete=models.CASCADE)
    payment_verification_status = models.CharField(default="unverified", max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    
class LeadOperationStatus(models.Model):
    lead = models.ForeignKey(Lead, related_name="operations_details", on_delete=models.CASCADE)
    added_to_group = models.BooleanField(default=False)
    registered_on_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    