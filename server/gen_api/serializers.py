from rest_framework import serializers

class ProofSerializer(serializers.Serializer):
    field = serializers.CharField()
    id = serializers.IntegerField()
    