# Generated by Django 3.2.20 on 2023-12-14 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_auto_20231214_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
