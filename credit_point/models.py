from django.db import models
from app.models import Order
from payment.models import Payment
from django.contrib.auth import get_user_model


User = get_user_model()

class CreditPointRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='credit_point_user')
    order_payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='credit_point_order')
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=100)
    credit_point_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
