# Generated by Django 3.2.20 on 2023-08-29 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('send_email_message', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sendemailmessage',
            old_name='created_at',
            new_name='timestamp',
        ),
        migrations.RemoveField(
            model_name='sendemailmessage',
            name='delivered_at',
        ),
        migrations.RemoveField(
            model_name='sendemailmessage',
            name='inbox',
        ),
        migrations.RemoveField(
            model_name='sendemailmessage',
            name='is_delivered',
        ),
        migrations.RemoveField(
            model_name='sendemailmessage',
            name='title',
        ),
        migrations.RemoveField(
            model_name='sendemailmessage',
            name='user',
        ),
        migrations.AddField(
            model_name='sendemailmessage',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sendemailmessage',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sendemailmessage',
            name='subject',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sendemailmessage',
            name='message',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
