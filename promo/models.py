# yourapp/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateTimeField()


class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="referred_user")
    referral_code = models.CharField(max_length=20, unique=True)
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="referred_by")
