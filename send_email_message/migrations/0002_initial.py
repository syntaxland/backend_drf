# Generated by Django 3.2.20 on 2023-09-16 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('send_email_message', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='sendemailmessage',
            name='receiver_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sendemailmessage',
            name='sender_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
