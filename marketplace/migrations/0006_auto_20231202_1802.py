# Generated by Django 3.2.20 on 2023-12-02 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0005_rename_campaign_duration_postfreead_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfreead',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='./media/marketplace'),
        ),
        migrations.AlterField(
            model_name='postfreead',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='./media/marketplace'),
        ),
        migrations.AlterField(
            model_name='postfreead',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='./media/marketplace'),
        ),
    ]