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
    
    def check_lead_update_status(self):
        sale_details = self.sale_details.first()
        print(self, sale_details)
        print(sale_details)
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
