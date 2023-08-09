from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

