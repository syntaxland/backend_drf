# Generated by Django 3.2.20 on 2023-12-02 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_auto_20231202_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfreead',
            name='duration',
            field=models.CharField(blank=True, choices=[('0 day', '0 day'), ('1 day', '1 day'), ('2 days', '2 days'), ('3 days', '3 days'), ('5 days', '5 days'), ('1 week', '1 week'), ('2 weeks', '2 weeks'), ('1 month', '1 month')], default='1 day', max_length=100, null=True),
        ),
    ]