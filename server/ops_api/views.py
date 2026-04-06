from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from admin_api.models import Lead, LeadOperationStatus
from admin_api.serializers import LeadOperationStatusPatchSerializer, LeadGetSerializer

class LeadView(APIView):
    def get(self, request):
        """Get lead details for operations team"""
        lead_id = request.GET.get('id')
        if not lead_id:
            return Response({
                "error": "Lead ID is required",
                "status": "error"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            lead = Lead.objects.get(id=lead_id)
            if not lead:
                return Response({
                    "error": "Lead not found",
                    "status": "error"
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                "lead": LeadGetSerializer(lead).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": str(e),
                "status": "error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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