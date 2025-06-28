from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from . import excelService 
from admin_api.models import Lead, Batch
from admin_api.serializers import (
    EmployeeGetSerializer,
    EmployeePatchSerializer,
    LeadGetSerializer,
    LeadBoardScorePatchSerializer,
    LeadAccountStatusPatchSerializer,
    LeadOperationStatusPatchSerializer,
    LeadPatchSerializer,
    BatchGetSerializer,
    BatchPatchSerializer,
    BatchPostSerializer
)
from auth_api.serializers import UserGetSerializer        
from auth_api.models import Employee, User
from django.http import FileResponse, Http404
import os


class DownloadDatabaseFile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # filepath = '/absolute/path/to/db.sqlite3'
        filepath = os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3')
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            raise Http404("Database file not found")

        return FileResponse(
            open(filepath, 'rb'),
            as_attachment=True,
            filename='db.sqlite3'
        )
class LeadSheetView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        lead_sheet = request.FILES.get('file')
        excelService.get_leads(lead_sheet)
        leads = Lead.objects.all()
        # for lead in leads:
        #     print(lead.name, lead.created_at)
        return Response({
            'msg': 'Obtained Leads',
            'leads': [LeadGetSerializer(lead).data for lead in leads] 
        }, status=status.HTTP_200_OK)
        
    def get(self, request):
        leads = Lead.objects.all()
        leads = [LeadGetSerializer(lead).data for lead in leads]
        # print(leads)
        return Response({
            "leads": leads
        }, status=status.HTTP_200_OK)
        
    def patch(self, request): ## edit one lead 
        print(f"patch request: {request.data}")
        lead = Lead.objects.filter(id=request.data.get('id')).first()
        serializer = LeadPatchSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        for field in ['assigned_to', 'status', 'source']:
            if field in serializer.validated_data:
                setattr(lead, field, serializer.validated_data[field])
        lead.save()
        print(lead)
        return Response({
            'msg': 'Lead edited',
            "lead": LeadGetSerializer(lead).data 
        }, status=status.HTTP_200_OK)
        

class SaleView(APIView): 
    permission_classes = [IsAuthenticated]
    def get(self, request):
        employees = User.objects.filter(is_admin=False)
        print(employees)
        emps = [UserGetSerializer(employee).data for employee in employees]
        print(emps)
        return Response({
            "msg": "all Employees",
            "employees": emps 
        })
        
    def patch(self, request): ## edit a sales employee
        emp = Employee.objects.filter(user=request.data.get('userID'))
        serializer = EmployeePatchSerializer(data=request.data)
        serializer.is_valid()
        for field in ['allot']:
            if field in serializer.validated_data:
                setattr(emp, field, serializer.validated_data[field])
        emp.save()
        print(emp)
        return Response({
            'msg': 'Employee Updated'
        }, status=status.HTTP_200_OK)
    
            
class ResetAllotLeads(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        emps = Employee.objects.filter(type="sales")
        for emp in emps:
            emp.allot = 0
            emp.save()
            print(emp)
        return Response({
            'msg': 'alloted leads reset'
        }, status=status.HTTP_200_OK)
        
            
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        total_leads = Lead.objects.all().count()
        dnp_leads = Lead.objects.filter(status='dnp').count()
        active_leads = total_leads - dnp_leads
        closed_leads = Lead.objects.filter(status="closed-sucess")
        converted_leads = 0
        for lead in closed_leads:
            lead.sale_details.status = 'verified'
            converted_leads += 1
        return Response({
            'converted_leads': converted_leads,
            'dnp_leads': dnp_leads,
            'active_leads': active_leads,
            'total_leads': total_leads
        }, status=status.HTTP_200_OK)


class EmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = User.objects.filter(is_admin=False)
        emps = [UserGetSerializer(user).data for user in users]
        return Response({
            'employees': emps
        })
    def patch(self, request):
        emp = Employee.objects.filter(id=request.data.get('id')).first()
        print(emp)
        serializer = EmployeePatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        setattr(emp, 'allot', serializer.validated_data.get('allot'))
        emp.save()
        
        return Response({
            'emp': EmployeeGetSerializer(emp).data 
        })
        

class BatchView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        batches = Batch.objects.all()
        all_batches = [BatchGetSerializer(batch).data for batch in batches]
        return Response({
            'batches': all_batches
        })
    
    def post(self, request):
        serializer = BatchPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch = serializer.save()
        
        return Response({
            'msg': 'New Batch added success',
            'batch': BatchGetSerializer(batch).data
        })
    
    def patch(self, request):
        batch = Batch.objects.filter(id=request.data.get('batchID')).first()
        serializer = BatchPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for field in ['price', 'books_price', 'status', 'name']:
            if field in serializer.validated_data:
                setattr(batch, field, serializer.validated_data[field])
        batch.save()
        print(batch)
        return Response({
            'msg': 'Batch updated success'
        })


class ClosedSalesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        closed_leads = Lead.objects.filter(status='closed-success')
        sale_completed_leads = [lead.sale_details.status == 'verified' for lead in closed_leads]
        leads = [LeadGetSerializer(lead).data for lead in sale_completed_leads] 
        revenue = 0
        print(leads)
        for lead in leads:
            print(lead)
        return Response({
            'msg': 'closed leads fetched',
            'revenue': revenue,
            'leads': leads      
        })
        
        