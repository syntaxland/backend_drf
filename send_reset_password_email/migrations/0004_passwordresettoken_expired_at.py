# Generated by Django 4.1.4 on 2023-08-16 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('send_reset_password_email', '0003_remove_passwordresettoken_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordresettoken',
            name='expired_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
