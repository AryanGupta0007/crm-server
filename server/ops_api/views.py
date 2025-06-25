from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from admin_api.models import Lead, LeadOperationStatus
from admin_api.serializers import LeadOperationStatusPatchSerializer

class LeadView(APIView):
    def patch(self, request):
        lead = Lead.objects.filter(id=request.data.get('leadID')).first()
        serializer = LeadOperationStatusPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        operation = lead.operation_details 
        for field in ['registered_on_app', 'added_to_group']:
            if field in serializer.validated_data:
                setattr(operation, field, serializer.validated_data[field])
        operation.save()
        return Response({
            "msg": "lead updated"
        }, status=status.HTTP_200_OK)