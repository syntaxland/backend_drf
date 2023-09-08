# Generated by Django 3.2.20 on 2023-09-04 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_product_save_count'),
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_products',
            field=models.ManyToManyField(related_name='favorited_by', to='app.Product'),
        ),
    ]
