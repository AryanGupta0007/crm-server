from rest_framework import status
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from admin_api.serializers import (
    LeadGetSerializer,
    BatchGetSerializer
    )
from admin_api.models import Lead, Batch
from auth_api.models import User, Employee
from auth_api.serializers import (
    UserGetSerializer,
    EmployeeGetSerializer,
    )

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()
        return Response({
            "msg": "current user fetched",
            "user": UserGetSerializer(user).data
        })
        


class UnderReviewLeads(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        under_review_leads = Lead.objects.filter(sale_details__status="under-review").distinct()

        leads = [LeadGetSerializer(lead).data for lead in under_review_leads]
        return Response({
            "msg": "under review leads fetched",
            "leads": leads
        })
        
        
class BatchView(APIView):
    def get(self, request):
        batches = Batch.objects.all()
        all_batches = [BatchGetSerializer(batch).data for batch in batches]
        return Response({
            'batches': all_batches
        })