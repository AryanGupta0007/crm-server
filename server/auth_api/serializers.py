from rest_framework import serializers
from auth_api.models import User, Employee


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "password", "contact", "is_admin"]
    
    def validate(self, attrs):
        email = attrs.get('email')
        name = attrs.get('name')
        contact = attrs.get('contact')
        password = attrs.get('password')
        is_admin = attrs.get('is_admin')
        if not email or not  name or not contact or not password :
            raise serializers.ValidationError('Either email or name or contact number or password or type of the user is not defined')
        if (email): 
            if (User.objects.filter(email=email).exists()):
                raise serializers.ValidationError('user with this email already exists')
        if (contact): 
            if (User.objects.filter(contact=contact).exists()):
                raise serializers.ValidationError('user with this contact number already exists')
        return super().validate(attrs=attrs)
    
    def create(self, validated_data):
        email = validated_data.get('email')
        name = validated_data.get('name')
        contact = validated_data.get('contact')
        password = validated_data.get('password')
        if (validated_data.get('is_admin')):
            is_admin = validated_data.get(is_admin)
        else:
            is_admin = False
        user = User(email=email, name=name, contact=contact, is_admin=is_admin)
        user.set_password(password)
        print(f'created_user {user}')
        user.save()
        return user    

class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["type"]
    
    def validate(self, attrs):
        type = attrs.get('type')
        if not type :
            raise serializers.ValidationError('Type of employee not found')
        return attrs
    def create(self, validated_data):
        user = self.context.get('user')
        type = validated_data.get('type')
        emp = Employee(type=type, user=user)
        emp.save()
        return emp
    
class EmployeeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

            
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if not email or not password:
            raise serializers.ValidationError('Email or Password not found')
        if not (User.objects.filter(email=email).exists()):
            raise serializers.ValidationError('User doesnt exist')
        return super().validate(attrs=attrs)
    
    
class UserGetSerializer(serializers.ModelSerializer):
    employee_details = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = '__all__'
    def get_employee_details(self, obj):
        return EmployeeGetSerializer(obj.employee_details.first(), many=False).data
        
