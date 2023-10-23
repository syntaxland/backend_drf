# Generated by Django 3.2.20 on 2023-10-15 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support', '0011_auto_20231014_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supportticket',
            old_name='closed_at',
            new_name='modified',
        ),
        migrations.RemoveField(
            model_name='supportmessage',
            name='support_ticket',
        ),
        migrations.RemoveField(
            model_name='supportresponse',
            name='support_message',
        ),
        migrations.AddField(
            model_name='supportticket',
            name='message',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='supportticket',
            name='subject',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='supportticket',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_ticket_user', to=settings.AUTH_USER_MODEL),
        ),
    ]