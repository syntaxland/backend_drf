from rest_framework import serializers
from .models import CreditPoint, CreditPointRequest
from django.contrib.auth import get_user_model

User = get_user_model() 


class CreditPointRequestSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    class Meta:
        model = CreditPointRequest
        fields = '__all__'


class CreditPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPoint
        fields = "__all__"
