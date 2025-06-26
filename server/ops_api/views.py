from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from admin_api.models import Lead, LeadOperationStatus
from admin_api.serializers import LeadOperationStatusPatchSerializer, LeadGetSerializer

class LeadView(APIView):
    def patch(self, request):
        lead = Lead.objects.filter(id=request.data.get('id')).first()
        serializer = LeadOperationStatusPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        operation = lead.operations_details.first() 
        for field in ['registered_on_app', 'added_to_group']:
            if field in serializer.validated_data:
                setattr(operation, field, serializer.validated_data[field])
        operation.save()
        return Response({
            "msg": "lead updated",
            "lead": LeadGetSerializer(lead).data
        }, status=status.HTTP_200_OK)