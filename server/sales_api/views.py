from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from admin_api.models import Lead
from admin_api.serializers import LeadGetSerializer, LeadPatchSerializer,  LeadSaleStatusPatchSerializer, LeadBoardScorePatchSerializer

class LeadView(APIView):
    def patch(self, request):
        lead = Lead.objects.filter(id=request.data.get('id')).first()
        serializer = LeadPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
            
        for field in ['status']:
            if field in serializer.validated_data:
                setattr(lead, field, serializer.validated_data[field])
                    
        return Response({
            "msg": "Lead updated",
            "lead": LeadGetSerializer(lead).data
        }) 
    

class LeadSaleView(APIView):
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
            for field in ['batch', 'status', 'form_ss', 'discount', 'discount_ss', 'buy_books', 'books_ss', 'payment_ss', 'followUpDate', 'comment']:
                if field in serializer.validated_data:
                    setattr(lead_sale_details, field, serializer.validated_data[field])
            lead_sale_details.save()
        if (lead_sale_details.payment_ss and lead_sale_details.form_ss ):
            if (lead_sale_details.buy_books):
                if (lead_sale_details.books_ss):
                    if (lead_sale_details.discount):
                        if (lead_sale_details.discount_ss):
                            lead.status = 'under-review'
                    else:
                        lead.status = 'under-review'
            else: 
                if (lead_sale_details.discount):
                        if (lead_sale_details.discount_ss):
                            lead.status = 'under-review'
                else:
                    lead.status = 'under-review'
                    
                    
        return Response({
            "msg": "Lead updated",
            "lead": LeadGetSerializer(lead).data
        }) 
        
class LeadBoardScoreView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        lead = Lead.objects.filter(id=request.data.get('id')).first()
        serializer = LeadBoardScorePatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead_board_scroe = lead.board_score.first()
        if (lead_board_scroe):    
            for field in ['pcm_score', 'english_score',]:
                if field in serializer.validated_data:
                    setattr(lead_board_scroe, field, serializer.validated_data[field])
            lead_board_scroe.save()
                    
        return Response({
            "msg": "Lead updated",
            "lead": LeadGetSerializer(lead).data
        }) 
                