from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from auth_api.serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserGetSerializer,
    EmployeeCreateSerializer,
    EmployeeGetSerializer
    )
from auth_api.models import User, Employee
from .Utils import Utils

class UserView(APIView):
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserGetSerializer(user)
        emp = Employee.objects.filter(user=user).first()
        employee_serializer = EmployeeGetSerializer(emp) if emp else None
        if employee_serializer:
            print(employee_serializer.data)
        return Response(
            {
                "msg": "user obtained",
                "user": serializer.data,
                "employee": employee_serializer.data if employee_serializer else None
            }, status=status.HTTP_200_OK
            )
    
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        emp_serializer = EmployeeCreateSerializer(data=request.data, context={'user': user})
        emp_serializer.is_valid(raise_exception=True)
        emp_serializer.save()
        
        emp = Employee.objects.filter(user=user).first()
        print(emp)
        token = Utils.get_tokens_for_user(user=user)
            
        # user_serializer = UserGetSerializer(user)
        return Response(
            {
                "token": token,
                "user": UserGetSerializer(user).data,
                "msg": "User created",
                "emp": emp_serializer.data
            }, status=status.HTTP_200_OK)
    
    
    
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)    
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        print(f"serializer data: {serializer.data}")
        user = authenticate(email=email, password=password)
        if user is not None: 
            token = Utils.get_tokens_for_user(user=user) 
            
            emp_serializer = EmployeeGetSerializer(Employee.objects.filter(user=user).first())
            return Response(
            {
                "token": "jfsljfalsdjf",
                "msg": "User Logged Login",
                "user": UserGetSerializer(user).data,
                "emp": emp_serializer.data,
                "token": token
            }, status=status.HTTP_200_OK
            )
        return Response(
            {
                "msg": "Invalid credentials"
            }, status=status.HTTP_404_NOT_FOUND
            )     
            