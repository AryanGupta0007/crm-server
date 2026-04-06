from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from validators import validate_email_format, validate_phone_number, validate_name, validate_user_type


# Create your models here.
class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)
    
    def create_user(self, name, email, contact, type, password=None):
        if not email:
            raise ValueError('Users must have an email')
        
        # Validate input data
        validate_email_format(email)
        validate_phone_number(contact)
        validate_name(name)
        validate_user_type(type)
        
        # Check for uniqueness
        if self.filter(email=email).exists():
            raise ValueError('A user with this email already exists.')
        
        if self.filter(contact=contact).exists():
            raise ValueError('A user with this contact number already exists.')
        
        user = self.model(
            email=email.lower(),  # Normalize email
            name=name.strip(),
            type=type,
            contact=contact
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, contact, type, password=None):
        # Validate input data
        validate_email_format(email)
        validate_phone_number(contact)
        validate_name(name)
        
        user = self.model(
            type=type,
            name=name.strip(),
            email=email.lower(),
            contact=contact
        )
        user.set_password(password)
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'A user with this email address already exists.',
        }
    )
    name = models.CharField(
        max_length=72,
        error_messages={
            'max_length': 'Name cannot be longer than 72 characters.',
        }
    )
    contact = models.CharField(
        max_length=20,  # Increased for international numbers
        error_messages={
            'max_length': 'Contact number cannot be longer than 20 characters.',
        }
    )
    type = models.CharField(
        max_length=23, 
        default='sales',
        error_messages={
            'max_length': 'User type cannot be longer than 23 characters.',
        }
    )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    
    def clean(self):
        """Custom validation for model fields"""
        super().clean()
        validate_email_format(self.email)
        validate_phone_number(self.contact)
        validate_name(self.name)
        validate_user_type(self.type)
        
        # Normalize email
        self.email = self.email.lower()
        self.name = self.name.strip()
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation before saving
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"User Details: name: {self.name}, email: {self.email}, admin: {self.is_admin}, contact: {self.contact}"



class Employee(models.Model):
    user = models.ForeignKey(User, related_name="employee_details", on_delete=models.CASCADE)
    type = models.CharField(default="sales", max_length=23)
    allot = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"Emp Details: name: {self.user.name}, email: {self.user.email}, admin: {self.user.is_admin}, contact: {self.user.contact}, alloted_leads: {self.allot}, employee type: {self.type}"
