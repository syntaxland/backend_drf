# Generated by Django 3.2.20 on 2023-10-12 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0005_auto_20231010_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportmessage',
            name='modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]