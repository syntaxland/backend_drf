# Generated by Django 3.2.20 on 2023-09-18 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_order_total_promo_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_promo_price',
            new_name='promo_total_price',
        ),
    ]
