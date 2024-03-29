# Generated by Django 3.2.20 on 2023-11-24 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketplaceSellerPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='media/sellers/')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photo_seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MarketPlaceSellerAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100, null=True)),
                ('business_status', models.CharField(choices=[('Registered', 'Registered'), ('Unregistered', 'Unregistered')], max_length=225, null=True)),
                ('business_reg_num', models.CharField(blank=True, max_length=50, null=True)),
                ('business_address', models.CharField(max_length=225, null=True)),
                ('staff_size', models.CharField(choices=[('Small', 'Small (1-50 employees)'), ('Medium', 'Medium (51-250 employees)'), ('Large', 'Large (251+ employees)')], max_length=50, null=True)),
                ('business_industry', models.CharField(choices=[('Information Technology', 'Information Technology'), ('Healthcare', 'Healthcare'), ('Finance', 'Finance'), ('Education', 'Education'), ('Retail', 'Retail'), ('Manufacturing', 'Manufacturing'), ('Services', 'Services'), ('Entertainment', 'Entertainment'), ('Food', 'Food & Beverage'), ('Travel', 'Travel & Tourism'), ('Real Estate', 'Real Estate'), ('Construction', 'Construction'), ('Automotive', 'Automotive'), ('Agriculture', 'Agriculture'), ('Energy', 'Energy'), ('Environmental', 'Environmental'), ('Government', 'Government'), ('Nonprofit', 'Nonprofit'), ('Others', 'Others')], max_length=50, null=True)),
                ('business_category', models.CharField(choices=[('Startup', 'Startup'), ('Small Business', 'Small Business'), ('Medium Business', 'Medium Business'), ('Large Business', 'Large Business'), ('Corporation', 'Corporation'), ('Sole Proprietorship', 'Sole Proprietorship'), ('Partnership', 'Partnership'), ('Franchise', 'Franchise'), ('Family Owned', 'Family Owned'), ('Online Business', 'Online Business'), ('Brick and Mortar', 'Brick and Mortar'), ('Service Provider', 'Service Provider'), ('Retailer', 'Retailer'), ('Wholesaler', 'Wholesaler'), ('Manufacturer', 'Manufacturer'), ('Restaurant', 'Restaurant'), ('Hospitality', 'Hospitality'), ('Healthcare', 'Healthcare'), ('Education', 'Education'), ('Tech', 'Tech'), ('Creative', 'Creative'), ('Entertainment', 'Entertainment'), ('Travel', 'Travel'), ('Construction', 'Construction'), ('Automotive', 'Automotive'), ('Agriculture', 'Agriculture'), ('Energy', 'Energy'), ('Environmental', 'Environmental'), ('Government', 'Government'), ('Nonprofit', 'Nonprofit'), ('Others', 'Others')], max_length=50, null=True)),
                ('business_description', models.TextField(blank=True, max_length=225, null=True)),
                ('business_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('business_website', models.CharField(blank=True, max_length=225, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('id_type', models.CharField(blank=True, choices=[('NIN', 'NIN'), ('Intl Passport', 'Intl Passport'), ('Driving License', 'Driving License'), ('Govt Issued ID', 'Govt Issued ID')], max_length=50, null=True)),
                ('id_number', models.CharField(max_length=30, null=True)),
                ('id_card_image', models.ImageField(upload_to='media/sellers/')),
                ('dob', models.CharField(blank=True, max_length=225, null=True)),
                ('home_address', models.CharField(blank=True, max_length=225, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller_account_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
