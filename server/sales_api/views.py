from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from admin_api.models import Lead
from admin_api.serializers import LeadGetSerializer, LeadSaleStatusPatchSerializer


class LeadView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(f'request.user: {request.user}')
        leads = Lead.objects.filter(assigned_to=request.user)
        all_leads = [LeadGetSerializer(lead).data for lead in leads]
        return Response({
            'msg': 'user leads fetched',
            'leads': all_leads
        })
    def patch(self, request):
        lead = Lead.objects.filter(id=request.data.get('id')).first()
        serializer = LeadSaleStatusPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead_sale_details = lead.sale_details.first()
        if (lead_sale_details):    
            for field in ['batch', 'status', 'form_ss', 'discount', 'discount_ss', 'buy_books', 'books_ss', 'payment_ss']:
                if field in serializer.validated_data:
                    setattr(lead_sale_details, field, serializer.validated_data[field])
            lead_sale_details.save()
        else:
            serializer = LeadSaleStatusPostSerializer
        
        return Response({
            "msg": "Lead updated",
            "lead": LeadGetSerializer(lead).data
        }) 
        