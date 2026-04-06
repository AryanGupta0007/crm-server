from rest_framework import serializers
from django.core.exceptions import ValidationError
from validators import (
    validate_email_format, validate_phone_number, validate_name, 
    validate_user_type, validate_lead_status, validate_batch_status,
    validate_price, validate_image_file, validate_excel_file
)
from auth_api.models import User, Employee
from admin_api.models import Lead, Batch


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user creation with validation"""
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'contact', 'type', 'password', 'confirm_password']
    
    def validate_email(self, value):
        """Validate email format and uniqueness"""
        validate_email_format(value)
        
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        
        return value.lower()
    
    def validate_contact(self, value):
        """Validate phone number format and uniqueness"""
        validate_phone_number(value)
        
        if User.objects.filter(contact=value).exists():
            raise serializers.ValidationError('A user with this contact number already exists.')
        
        return value
    
    def validate_name(self, value):
        """Validate name format"""
        validate_name(value)
        return value.strip()
    
    def validate_type(self, value):
        """Validate user type"""
        validate_user_type(value)
        return value
    
    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError('Password must contain at least one digit.')
        
        if not any(c.isalpha() for c in value):
            raise serializers.ValidationError('Password must contain at least one letter.')
        
        return value
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Passwords do not match.')
        
        return attrs
    
    def create(self, validated_data):
        """Create user with validated data"""
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user updates with validation"""
    
    class Meta:
        model = User
        fields = ['name', 'contact', 'type']
    
    def validate_contact(self, value):
        """Validate phone number format and uniqueness (excluding current user)"""
        validate_phone_number(value)
        
        if User.objects.filter(contact=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('This contact number is already registered.')
        
        return value
    
    def validate_name(self, value):
        """Validate name format"""
        validate_name(value)
        return value.strip()
    
    def validate_type(self, value):
        """Validate user type"""
        validate_user_type(value)
        return value


class LeadCreateSerializer(serializers.ModelSerializer):
    """Serializer for lead creation with validation"""
    
    class Meta:
        model = Lead
        fields = ['name', 'contact_number', 'source', 'status', 'assigned_to']
    
    def validate_name(self, value):
        """Validate name format"""
        validate_name(value)
        return value.strip()
    
    def validate_contact_number(self, value):
        """Validate phone number format and uniqueness"""
        validate_phone_number(value)
        
        if Lead.objects.filter(contact_number=value).exists():
            raise serializers.ValidationError('A lead with this contact number already exists.')
        
        return value
    
    def validate_status(self, value):
        """Validate lead status"""
        validate_lead_status(value)
        return value
    
    def validate_assigned_to(self, value):
        """Validate assigned user is a sales user"""
        if value and value.type != 'sales':
            raise serializers.ValidationError('Leads can only be assigned to sales users.')
        
        return value


class LeadUpdateSerializer(serializers.ModelSerializer):
    """Serializer for lead updates with validation"""
    
    class Meta:
        model = Lead
        fields = ['name', 'source', 'status', 'assigned_to']
    
    def validate_name(self, value):
        """Validate name format"""
        validate_name(value)
        return value.strip()
    
    def validate_status(self, value):
        """Validate lead status"""
        validate_lead_status(value)
        return value
    
    def validate_assigned_to(self, value):
        """Validate assigned user is a sales user"""
        if value and value.type != 'sales':
            raise serializers.ValidationError('Leads can only be assigned to sales users.')
        
        return value


class BatchCreateSerializer(serializers.ModelSerializer):
    """Serializer for batch creation with validation"""
    
    class Meta:
        model = Batch
        fields = ['name', 'book_price', 'price', 'status']
    
    def validate_name(self, value):
        """Validate batch name format and uniqueness"""
        validate_batch_name(value)
        
        if Batch.objects.filter(name=value).exists():
            raise serializers.ValidationError('A batch with this name already exists.')
        
        return value.strip()
    
    def validate_book_price(self, value):
        """Validate book price"""
        validate_price(value)
        return value
    
    def validate_price(self, value):
        """Validate total price"""
        validate_price(value)
        return value
    
    def validate_status(self, value):
        """Validate batch status"""
        validate_batch_status(value)
        return value
    
    def validate(self, attrs):
        """Business logic validation"""
        if attrs['price'] < attrs['book_price']:
            raise serializers.ValidationError('Total price cannot be less than book price.')
        
        return attrs


class BatchUpdateSerializer(serializers.ModelSerializer):
    """Serializer for batch updates with validation"""
    
    class Meta:
        model = Batch
        fields = ['name', 'book_price', 'price', 'status']
    
    def validate_name(self, value):
        """Validate batch name format and uniqueness (excluding current batch)"""
        validate_batch_name(value)
        
        if Batch.objects.filter(name=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('A batch with this name already exists.')
        
        return value.strip()
    
    def validate_book_price(self, value):
        """Validate book price"""
        validate_price(value)
        return value
    
    def validate_price(self, value):
        """Validate total price"""
        validate_price(value)
        return value
    
    def validate_status(self, value):
        """Validate batch status"""
        validate_batch_status(value)
        return value
    
    def validate(self, attrs):
        """Business logic validation"""
        if 'price' in attrs and 'book_price' in attrs:
            if attrs['price'] < attrs['book_price']:
                raise serializers.ValidationError('Total price cannot be less than book price.')
        elif 'price' in attrs and attrs['price'] < self.instance.book_price:
            raise serializers.ValidationError('Total price cannot be less than book price.')
        elif 'book_price' in attrs and self.instance.price < attrs['book_price']:
            raise serializers.ValidationError('Total price cannot be less than book price.')
        
        return attrs


class FileUploadSerializer(serializers.Serializer):
    """Serializer for file uploads with validation"""
    file = serializers.FileField()
    file_type = serializers.ChoiceField(choices=['image', 'excel'])
    
    def validate_file(self, value):
        """Validate file based on type"""
        file_type = self.initial_data.get('file_type', 'image')
        
        if file_type == 'image':
            validate_image_file(value)
        elif file_type == 'excel':
            validate_excel_file(value)
        
        return value


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """Serializer for employee creation with validation"""
    
    class Meta:
        model = Employee
        fields = ['user', 'type', 'allot']
    
    def validate_user(self, value):
        """Validate user doesn't already have an employee record"""
        if Employee.objects.filter(user=value).exists():
            raise serializers.ValidationError('This user already has an employee record.')
        
        return value
    
    def validate_type(self, value):
        """Validate employee type"""
        validate_user_type(value)
        return value
    
    def validate_allot(self, value):
        """Validate allotment is non-negative"""
        if value < 0:
            raise serializers.ValidationError('Allotment cannot be negative.')
        
        return value


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    """Serializer for employee updates with validation"""
    
    class Meta:
        model = Employee
        fields = ['type', 'allot']
    
    def validate_type(self, value):
        """Validate employee type"""
        validate_user_type(value)
        return value
    
    def validate_allot(self, value):
        """Validate allotment is non-negative"""
        if value < 0:
            raise serializers.ValidationError('Allotment cannot be negative.')
        
        return value
