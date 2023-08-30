from django.db import models
# from django.contrib.auth.models import User
from app.models import Order
from django.contrib.auth import get_user_model

User = get_user_model() 


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
