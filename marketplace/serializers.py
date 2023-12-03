# marketplace/serializers.py
from rest_framework import serializers
from .models import MarketPlaceSellerAccount, MarketplaceSellerPhoto, PostFreeAd, PostPaidAd


class MarketPlaceSellerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPlaceSellerAccount
        fields = '__all__'
        extra_kwargs = {'id_card_image': {'required': True}}


class MarketplaceSellerPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceSellerPhoto
        fields = '__all__'
        extra_kwargs = {'photo': {'required': True}}


class PostFreeAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFreeAd
        fields = '__all__'
        extra_kwargs = {'image1': {'required': True}, 'image2': {'required': True}, 'image3': {'required': True}}


class PostPaidAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPaidAd
        fields = '__all__'
        extra_kwargs = {'image1': {'required': True}, 'image2': {'required': True}, 'image3': {'required': True}}
