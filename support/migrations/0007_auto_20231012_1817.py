# Generated by Django 3.2.20 on 2023-10-12 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0006_alter_supportmessage_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportmessage',
            name='category',
        ),
        migrations.AddField(
            model_name='supportticket',
            name='category',
            field=models.CharField(blank=True, choices=[('otp', 'OTP'), ('payments', 'Payments'), ('transactions', 'Transactions'), ('payouts', 'Payouts'), ('services', 'Services'), ('credit_points', 'Credit Points'), ('account_funds', 'Account Funds'), ('referrals', 'Referrals'), ('others', 'Others')], max_length=225, null=True),
        ),
    ]