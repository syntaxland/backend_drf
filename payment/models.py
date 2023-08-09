from django.db import models
# from django.contrib.auth.models import User
from app.models import Order
# from user_profile.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model() 


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=10, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=10, unique=True, blank=True)
    # user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
