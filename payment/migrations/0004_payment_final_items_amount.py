# Generated by Django 3.2.20 on 2023-09-19 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20230918_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='final_items_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
