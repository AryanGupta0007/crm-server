from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)
    def create_user(self, name, email, contact, type, password=None):
        if not email:
            return ValueError('Users must have a email')
        user = self.model(
            email=email,
            name=name,
            type=type,
            contact=contact
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, contact, type, password=None):
        user = self.model(
            type=type,
            name=name,
            email=email,
            contact=contact
        )
        user.set_password(password)
        user.is_admin=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=72)
    contact = models.CharField(max_length=14)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    
    def __str__(self):
        return f"User Details: name: {self.name}, email: {self.email}, admin: {self.is_admin}, contact: {self.contact}"



class Employee(models.Model):
    user = models.ForeignKey(User, related_name="employee_details", on_delete=models.CASCADE)
    type = models.CharField(default="sales", max_length=23)
    allot = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"Emp Details: name: {self.user.name}, email: {self.user.email}, admin: {self.user.is_admin}, contact: {self.user.contact}, alloted_leads: {self.allot}, employee type: {self.type}"