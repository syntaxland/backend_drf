# Generated by Django 3.2.20 on 2023-12-28 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0026_auto_20231228_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='postfreead',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postfreead',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postfreead',
            name='state_province',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postpaidad',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postpaidad',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postpaidad',
            name='state_province',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
