# payment/models.py
from django.db import models
from app.models import Order
from django.contrib.auth import get_user_model

User = get_user_model() 


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='order_payment') 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    items_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_items_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    promo_code_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    promo_code_discount_percentage = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    final_total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reference = models.CharField(max_length=10, unique=True, blank=True) 
    payment_provider = models.CharField(max_length=50, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - NGN {self.amount} - {self.order.order_id}"
