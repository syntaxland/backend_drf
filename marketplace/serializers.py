# serializers.py
from rest_framework import serializers
from .models import Ad, Image, Seller
from user_profile.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Seller
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        seller = Seller.objects.create(user=user, **validated_data)
        return seller


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)

class AdSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Ad
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        ad = Ad.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(ad=ad, **image_data)
        return ad
