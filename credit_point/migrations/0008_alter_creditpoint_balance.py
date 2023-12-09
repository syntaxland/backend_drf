# Generated by Django 3.2.20 on 2023-12-04 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_point', '0007_alter_creditpoint_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditpoint',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
    ]