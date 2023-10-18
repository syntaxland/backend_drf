# Generated by Django 3.2.20 on 2023-10-15 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='category',
            field=models.CharField(blank=True, choices=[('support', 'Support'), ('billing', 'Billing'), ('abuse', 'Abuse'), ('otp', 'OTP'), ('payments', 'Payments'), ('transactions', 'Transactions'), ('payouts', 'Payouts'), ('services', 'Services'), ('credit_points', 'Credit Points'), ('account_funds', 'Account Funds'), ('referrals', 'Referrals'), ('others', 'Others')], max_length=225, null=True),
        ),
    ]
