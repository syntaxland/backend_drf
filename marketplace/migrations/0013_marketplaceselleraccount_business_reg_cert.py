# Generated by Django 3.2.20 on 2023-12-04 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0012_postpaidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketplaceselleraccount',
            name='business_reg_cert',
            field=models.ImageField(blank=True, null=True, upload_to='media/sellers/'),
        ),
    ]