from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from admin_api.models import Lead, LeadOperationStatus
from admin_api.serializers import LeadAccountStatusPatchSerializer

class LeadView(APIView):
    def patch(self, request):
        lead = Lead.objects.filter(id=request.data.get('leadID')).first()
        
        serializer = LeadAccountStatusPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = lead.account_details  # assume it's a related model instance
        for field in ['payment_verification_status']:
            if field in serializer.validated_data:
                setattr(account, field, serializer.validated_data[field])
        account.save()
        print(lead)
        return Response({
            "msg": "lead updated"
        }, status=status.HTTP_200_OK)