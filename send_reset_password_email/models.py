from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class PasswordResetToken(models.Model):
    token = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        return self.created_at >= timezone.now() - timezone.timedelta(minutes=30)

    def generate_token(self):
        self.token = get_random_string(length=32)
        self.created_at = timezone.now()
        self.save()

    class Meta:
        default_related_name = 'password_reset_tokens'
