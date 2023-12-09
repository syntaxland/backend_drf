# Generated by Django 3.2.20 on 2023-12-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0018_auto_20231209_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postfreead',
            name='seller_photo',
        ),
        migrations.RemoveField(
            model_name='postpaidad',
            name='seller_photo',
        ),
        migrations.AlterField(
            model_name='postfreead',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='postpaidad',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]