# Generated by Django 3.2.20 on 2023-12-14 10:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promo', '0004_alter_referralbonus_referral_credit_points_bonus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='referred_users',
            field=models.ManyToManyField(default=0, related_name='referred_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
