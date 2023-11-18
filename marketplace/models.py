# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class Ad(models.Model):
    product_name = models.CharField(max_length=80)
    category = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    ad_type = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    youtube_link = models.URLField(blank=True, null=True)
    campaign_duration = models.CharField(max_length=20)
    images = models.ManyToManyField('Image', related_name='ads')

    def __str__(self):
        return self.product_name

class Image(models.Model):
    image = models.ImageField(upload_to='ad_images/')

    def __str__(self):
        return f'Image {self.pk}'
