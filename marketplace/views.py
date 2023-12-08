# marketplace/views.py 
from decimal import Decimal
from datetime import datetime, timedelta, timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from credit_point.models import CreditPoint
from .models import MarketPlaceSellerAccount, MarketplaceSellerPhoto, PostFreeAd, PostPaidAd, PaysofterApiKey
from .serializers import MarketPlaceSellerAccountSerializer, MarketplaceSellerPhotoSerializer, PostFreeAdSerializer, PostPaidAdSerializer, PaysofterApiKeySerializer

from django.contrib.auth import get_user_model

User = get_user_model()

 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_marketplace_seller(request):
    seller, created = MarketPlaceSellerAccount.objects.get_or_create(seller=request.user)
    serializer = MarketPlaceSellerAccountSerializer(instance=seller, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_marketplace_seller_photo(request):
    seller=request.user
    data=request.data
    print('seller:', seller)
    print('data:', data)
    photo, created = MarketplaceSellerPhoto.objects.get_or_create(seller=seller)
    serializer = MarketplaceSellerPhotoSerializer(instance=photo, data=data)
    if serializer.is_valid():
        serializer.save()

        seller.is_marketplace_seller = True
        seller.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_free_ad(request):
    seller = request.user
    data = request.data
    serializer = PostFreeAdSerializer(data=data)


    try:
        free_ad_count = PostFreeAd.objects.filter(seller=seller).count()
        print('free_ad_count:', free_ad_count)
        if free_ad_count >= 3:
            return Response({'detail': f'You can only post a maximum of 3 free ads. You have posted {free_ad_count} free ads.'}, status=status.HTTP_400_BAD_REQUEST) 
    except User.DoesNotExist:
        pass

    if serializer.is_valid():        
        ad = serializer.save(seller=seller)

        if ad.duration:
            durations_mapping = {
                '0 day': timedelta(hours=0),
                '1 day': timedelta(hours=24),
                '2 days': timedelta(days=2),
                '3 days': timedelta(days=3),
                '5 days': timedelta(days=5),
                '1 week': timedelta(weeks=1),
                '2 weeks': timedelta(weeks=2),
                '1 month': timedelta(days=30),
            }

            ad.duration_hours = durations_mapping.get(ad.duration, timedelta(hours=0))
            ad.expiration_date = datetime.now() + ad.duration_hours

        ad.is_active = True
        ad.save()

        return Response({'success': f'Ad created successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_paid_ad(request):
    seller = request.user
    data = request.data 
    serializer = PostPaidAdSerializer(data=data)

    try:
        credit_point = CreditPoint.objects.get(user=seller)
        credit_point_balance = credit_point.balance

        print('credit_point_balance:', credit_point_balance)
        if credit_point_balance < 24:
            return Response({'detail': f'Your credit point credit point balance of {credit_point_balance} is too low. You need at least 24 cps to place a paid ad.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        pass

    if serializer.is_valid():        
        ad = serializer.save(seller=seller)

        if ad.duration:
            durations_mapping = {
                '0 day': timedelta(hours=0),
                '1 day': timedelta(hours=24),
                '2 days': timedelta(days=2),
                '3 days': timedelta(days=3),
                '5 days': timedelta(days=5),
                '1 week': timedelta(weeks=1),
                '2 weeks': timedelta(weeks=2),
                '1 month': timedelta(days=30),
            }

            ad.duration_hours = durations_mapping.get(ad.duration, timedelta(hours=0))
            ad.expiration_date = datetime.now() + ad.duration_hours

        ad.is_active = True
        ad.save()

        return Response({'success': f'Ad created successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def create_paid_ad(request):
#     seller = request.user
#     data = request.data
#     serializer = PostPaidAdSerializer(data=data)

#     try:
#         credit_point = CreditPoint.objects.get(user=seller)
#         credit_point_balance = credit_point.balance
#         print('credit_point_balance:', credit_point_balance)

#         if serializer.is_valid():
#             ad_duration = serializer.validated_data.get('duration', None)
#             print('ad_duration:', ad_duration)

#             if ad_duration:
#                 durations_mapping = {
#                     '1 day': 24,
#                     '2 days': 48,
#                     '3 days': 72,
#                     '5 days': 120,
#                     '1 week': 180,
#                     '2 weeks': 360,
#                     '1 month': 720,
#                 }

#                 required_cps = durations_mapping.get(ad_duration, 0)

#                 if credit_point_balance < required_cps:
#                     return Response({
#                         'detail': f'Your credit point balance of {credit_point_balance} is too low. You need at least {required_cps} cps to place a paid ad for {ad_duration}.'
#                     }, status=status.HTTP_400_BAD_REQUEST)

#             ad = serializer.save(seller=seller)

#             if ad_duration:
#                 ad_duration_hours = timedelta(hours=durations_mapping.get(ad_duration, 0))
#                 ad.expiration_date = datetime.now() + ad_duration_hours
#                 ad.is_active = True
#                 ad.save()

#                 return Response({'success': f'Ad created successfully.'}, status=status.HTTP_201_CREATED)

#     except User.DoesNotExist:
#         pass

#     return Response({'detail': 'Error processing the request.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_marketplace_seller_account(request):
    user = request.user
    try:
        marketplace_seller_account = MarketPlaceSellerAccount.objects.get(seller=user)
        serializer = MarketPlaceSellerAccountSerializer(marketplace_seller_account)
        return Response(serializer.data)
    except MarketPlaceSellerAccount.DoesNotExist:
        return Response({'detail': 'Marketplace seller account not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_marketplace_seller_account(request):
    user = request.user
    data = request.data
    print('data:', data)
    try:
        marketplace_seller_account = MarketPlaceSellerAccount.objects.get(seller=user)
    except MarketPlaceSellerAccount.DoesNotExist:
        return Response({'detail': 'Marketplace seller account not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MarketPlaceSellerAccountSerializer(marketplace_seller_account, data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Marketplace seller account updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_marketplace_seller_photo(request):
    user = request.user
    try:
        marketplace_seller_photo = MarketplaceSellerPhoto.objects.get(seller=user)
        serializer = MarketplaceSellerPhotoSerializer(marketplace_seller_photo)
        return Response(serializer.data)
    except MarketplaceSellerPhoto.DoesNotExist:
        return Response({'detail': 'Marketplace seller photo not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_marketplace_seller_photo(request):
    user = request.user
    data = request.data
    print('data:', data)
    try:
        marketplace_seller_photo = MarketplaceSellerPhoto.objects.get(seller=user)
    except MarketplaceSellerPhoto.DoesNotExist:
        return Response({'detail': 'Marketplace seller photo not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MarketplaceSellerPhotoSerializer(marketplace_seller_photo, data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Marketplace seller photo updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_seller_free_ad(request):
    user = request.user
    current_datetime = datetime.now()
    try:
        free_ad = PostFreeAd.objects.filter(seller=user, expiration_date__gt=current_datetime)
        serializer = PostFreeAdSerializer(free_ad, many=True)
        return Response(serializer.data)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Free ad not found'}, status=status.HTTP_404_NOT_FOUND)
 

# @api_view(['GET'])
# @permission_classes([AllowAny])
# @parser_classes([MultiPartParser, FormParser])
# def get_free_ad_detail(request, pk):
#     try:
#         ad = PostFreeAd.objects.get(id=pk)
#         serializer = PostFreeAdSerializer(ad, many=False)
#         return Response(serializer.data)
#     except PostFreeAd.DoesNotExist:
#         return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def get_free_ad_detail(request, pk):
    seller_api_key = None  

    try:
        ad = PostFreeAd.objects.get(id=pk)
        seller = ad.seller
        
        api_key = PaysofterApiKey.objects.get(seller=seller)
        seller_api_key = api_key.live_api_key

        serializer = PostFreeAdSerializer(ad)
        return Response({'data': serializer.data, 'sellerApiKey': seller_api_key}, status=status.HTTP_200_OK)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_seller_free_ad(request, pk):
    user = request.user
    data = request.data
    print('data:', data)
    try:
        free_ad = MarketPlaceSellerAccount.objects.get(seller=user, pk=pk)
    except MarketPlaceSellerAccount.DoesNotExist:
        return Response({'detail': 'Free ad not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MarketPlaceSellerAccountSerializer(free_ad, data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Free ad updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_free_ad(request, pk):
    user = request.user
    try:
        ad = PostFreeAd.objects.get(seller=user, pk=pk)
        ad.delete()
        return Response({'detail': 'Ad deleted successfully.'})
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Ad not found.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def get_all_free_ad(request):
    current_datetime = datetime.now()
    try:
        free_ad = PostFreeAd.objects.filter(expiration_date__gt=current_datetime)
        serializer = PostFreeAdSerializer(free_ad, many=True)
        return Response(serializer.data)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Free ad not found'}, status=status.HTTP_404_NOT_FOUND)

        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_seller_paid_ad(request):
    user = request.user
    current_datetime = datetime.now()
    try:
        paid_ad = PostPaidAd.objects.filter(seller=user, expiration_date__gt=current_datetime)
        serializer = PostPaidAdSerializer(paid_ad, many=True)
        return Response(serializer.data)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Paid ad not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def get_paid_ad_detail(request, pk):
    seller_api_key = None  

    try:
        ad = PostPaidAd.objects.get(id=pk)
        seller = ad.seller

        api_key = PaysofterApiKey.objects.get(seller=seller)
        seller_api_key = api_key.live_api_key

        serializer = PostPaidAdSerializer(ad)
        return Response({'data': serializer.data, 'sellerApiKey': seller_api_key}, status=status.HTTP_200_OK)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_seller_paid_ad(request, pk):
    user = request.user
    data = request.data
    print('data:', data)
    try:
        paid_ad = PostPaidAd.objects.get(seller=user, pk=pk)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Paid ad not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PostPaidAdSerializer(paid_ad, data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Paid ad updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_paid_ad(request, pk):
    user = request.user
    try:
        ad = PostPaidAd.objects.get(seller=user, pk=pk)
        ad.delete()
        return Response({'detail': 'Ad deleted successfully.'})
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def get_all_paid_ad(request):
    current_datetime = datetime.now()
    try:
        paid_ad = PostPaidAd.objects.filter(expiration_date__gt=current_datetime)
        serializer = PostPaidAdSerializer(paid_ad, many=True)
        return Response(serializer.data)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Paid ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def save_seller_paysofter_api_key(request):
    user = request.user
    data = request.data
    print('data:', data)
    try:
        api_key = PaysofterApiKey.objects.get(seller=user)
    except PaysofterApiKey.DoesNotExist:
        return Response({'detail': 'Api key not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PaysofterApiKeySerializer(api_key, data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Api key updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_seller_paysofter_api_key(request):
    user = request.user
    try:
        api_key = PaysofterApiKey.objects.get(seller=user)
        serializer = PaysofterApiKeySerializer(api_key)
        return Response(serializer.data)
    except PaysofterApiKey.DoesNotExist:
        return Response({'detail': 'Api key not found'}, status=status.HTTP_404_NOT_FOUND)
