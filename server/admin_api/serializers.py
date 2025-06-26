from rest_framework import serializers
from admin_api.models import (
    Lead,
    LeadBoardScore,
    LeadAccountStatus,
    LeadOperationStatus,
    LeadSaleStatus, 
    Batch
    )
from auth_api.serializers import UserGetSerializer
from auth_api.models import Employee, User




class EmployeePatchSerializer(serializers.ModelSerializer):
    model = Employee
    fields = ['allot']

class GetLeadBoardScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadBoardScore
        fields = '__all__'


class GetLeadAccountStatus(serializers.ModelSerializer):
    class Meta:
        model = LeadAccountStatus
        fields = '__all__'


class GetLeadSaleStatus(serializers.ModelSerializer):
    class Meta:
        model = LeadSaleStatus
        fields = '__all__'


class GetLeadOperationStatus(serializers.ModelSerializer):
    class Meta:
        model = LeadOperationStatus
        fields = '__all__'

class LeadPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['assigned_to',  'source', 'status', 'followUpDate']


class LeadBoardScorePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadBoardScore
        fields = ['english_score', 'pcm_score', 'year']


class LeadAccountStatusPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadAccountStatus
        fields = ['payment_verification_status']


class LeadOperationStatusPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadOperationStatus
        exclude = ['created_at', 'updated_at', 'lead']



class LeadSaleStatusPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadSaleStatus
        exclude = ['created_at', 'updated_at', 'lead']


class LeadGetSerializer(serializers.ModelSerializer):
    assigned_to = UserGetSerializer()
    board_score = serializers.SerializerMethodField()
    sale_details = serializers.SerializerMethodField()
    account_details = serializers.SerializerMethodField()
    operations_details = serializers.SerializerMethodField()
    revenue = serializers.SerializerMethodField()
    class Meta:
        model = Lead
        fields =  [
            'id',
            'assigned_to',
            'name',
            'contact_number',
            'board_score',
            'sale_details',
            'account_details',
            'operations_details',
            'status',
            'source',
            'followUpDate',
            'created_at',
            'updated_at',
            'revenue'
            ]
    def get_revenue(self, obj):
        amount = 0
        print(f"sale_details: {obj.sale_details}")
        # if (obj.sale_details.batch):
        #     batch = obj.sale_details.batch
        #     batch_details = Batch.objects.filter(id=batch) 
        #     amount += batch_details.price
        #     if (obj.sale_details.buy_books):
        #         amount += batch_details.book_price
        #     # if (obj.sale_details.discount):
        #     #     amount += obj.sale_details.discount
        return amount
    
    def get_operations_details(self, obj):
        return GetLeadOperationStatus(obj.operations_details.first(), many=False).data
    
    def get_board_score(self, obj):
        return GetLeadBoardScoreSerializer(obj.board_score.first(), many=False).data
    
    def get_sale_details(self, obj):
        return GetLeadSaleStatus(obj.sale_details.first(), many=False).data    
    
    def get_account_details(self, obj):
        return GetLeadAccountStatus(obj.account_details.first(), many=False).data


class BatchGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch 
        fields = '__all__'    
        
class BatchPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['name', 'book_price', 'price', 'status']
    
    def validate(self, attrs):
        print(attrs)
        name = attrs.get('name')
        status = attrs.get('status')
        book_price = attrs.get('book_price')
        price = attrs.get('price')
        if not name:
            raise serializers.ValidationError("name")
        if  (book_price == ""):
            raise serializers.ValidationError("book_price is not jfsljfl")
        if (price == ""):
            raise serializers.ValidationError("price")
        if not status:
            raise serializers.ValidationError("status")
        return super().validate(attrs=attrs)
    
    def create(self, validated_data):
        name = validated_data.get('name')
        status = validated_data.get('status')
        book_price = validated_data.get('book_price')
        price = validated_data.get('price')
        print(validated_data)
        print(name, status, book_price, price)
        batch = Batch(name=name, status=status, book_price=book_price, price=price)
        batch.save()
        return batch
    
class BatchPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['status', 'book_price', 'price', 'name']