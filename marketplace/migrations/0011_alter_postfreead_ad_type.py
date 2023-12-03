# Generated by Django 3.2.20 on 2023-12-03 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0010_auto_20231203_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfreead',
            name='ad_type',
            field=models.CharField(blank=True, choices=[('Washing Machine', 'Washing Machine'), ('Refrigerator', 'Refrigerator'), ('Microwave', 'Microwave'), ('Coffee Machine', 'Coffee Machine'), ('Air Conditioner', 'Air Conditioner'), ('House', 'House'), ('Apartment', 'Apartment'), ('Land', 'Land'), ('Commercial Property', 'Commercial Property'), ('Laptop', 'Laptop'), ('Smartphone', 'Smartphone'), ('Camera', 'Camera'), ('Headphones', 'Headphones'), ('Television', 'Television'), ('Clothing', 'Clothing'), ('Shoes', 'Shoes'), ('Accessories', 'Accessories'), ('Car', 'Car'), ('Motorcycle', 'Motorcycle'), ('Bicycle', 'Bicycle'), ('Cleaning', 'Cleaning'), ('Plumbing', 'Plumbing'), ('Electrician', 'Electrician'), ('Catering', 'Catering'), ('Tutoring', 'Tutoring'), ('iPhone', 'iPhone'), ('Samsung', 'Samsung'), ('Google Pixel', 'Google Pixel'), ('OnePlus', 'OnePlus'), ('Skincare', 'Skincare'), ('Haircare', 'Haircare'), ('Makeup', 'Makeup'), ('Fitness Equipment', 'Fitness Equipment'), ('Soccer', 'Soccer'), ('Basketball', 'Basketball'), ('Tennis', 'Tennis'), ('Golf', 'Golf'), ('IT', 'IT'), ('Sales', 'Sales'), ('Marketing', 'Marketing'), ('Administrative', 'Administrative'), ('Toys', 'Toys'), ('Clothing Kids', 'Clothing'), ('Strollers', 'Strollers'), ('Farm Products', 'Farm Products'), ('Processed Food', 'Processed Food'), ('Beverages', 'Beverages'), ('Electronic Repair', 'Electronic Repair'), ('Appliance Repair', 'Appliance Repair'), ('Car Repair', 'Car Repair'), ('Power Tools', 'Power Tools'), ('Hand Tools', 'Hand Tools'), ('Kitchen Tools', 'Kitchen Tools'), ('Engineering', 'Engineering'), ('Marketing CVs', 'Marketing'), ('Design', 'Design'), ('Education', 'Education'), ('Dog', 'Dog'), ('Cat', 'Cat'), ('Fish', 'Fish'), ('Bird', 'Bird'), ('Others', 'Others')], max_length=100, null=True),
        ),
    ]
