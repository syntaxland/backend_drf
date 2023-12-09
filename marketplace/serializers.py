# marketplace/serializers.py
from rest_framework import serializers
from .models import MarketPlaceSellerAccount, MarketplaceSellerPhoto, PostFreeAd, PostPaidAd, PaysofterApiKey


class MarketPlaceSellerAccountSerializer(serializers.ModelSerializer):
    business_phone = serializers.CharField(source='seller.phone_number', read_only=True)
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
    seller_avatar_url = serializers.SerializerMethodField()

    seller_phone = serializers.CharField(source='seller.phone_number', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    seller_joined_since = serializers.CharField(source='seller.created_at', read_only=True)
    class Meta:
        model = PostFreeAd
        fields = '__all__'
        extra_kwargs = {'image1': {'required': True}, 'image2': {'required': True}, 'image3': {'required': True}}

    def get_seller_avatar_url(self, obj):
        request = self.context.get('request')
        return request and request.get('seller_avatar_url', None)
 

# class PostPaidAdSerializer(serializers.ModelSerializer):
#     seller_avatar = serializers.CharField(source='seller_photo.photo.url', read_only=True)
#     seller_phone = serializers.CharField(source='seller.phone_number', read_only=True)
#     seller_username = serializers.CharField(source='seller.username', read_only=True)
#     seller_joined_since = serializers.CharField(source='seller.created_at', read_only=True)
#     class Meta:
#         model = PostPaidAd
#         fields = '__all__'
#         extra_kwargs = {'image1': {'required': True}, 'image2': {'required': True}, 'image3': {'required': True}}


class PostPaidAdSerializer(serializers.ModelSerializer):
    seller_avatar_url = serializers.SerializerMethodField()

    seller_phone = serializers.CharField(source='seller.phone_number', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    seller_joined_since = serializers.CharField(source='seller.created_at', read_only=True)

    class Meta:
        model = PostPaidAd
        fields = '__all__'
        extra_kwargs = {'image1': {'required': True}, 'image2': {'required': True}, 'image3': {'required': True}}

    def get_seller_avatar_url(self, obj):
        request = self.context.get('request')
        return request and request.get('seller_avatar_url', None)


class PaysofterApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaysofterApiKey
        fields = '__all__'
