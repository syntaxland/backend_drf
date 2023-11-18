# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import Ad, Image, Seller
from .serializers import AdSerializer, ImageSerializer, SellerSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
def register_seller(request):
    if request.method == 'POST':
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def post_ad(request):
    if request.method == 'POST':
        ad_serializer = AdSerializer(data=request.data)
        if ad_serializer.is_valid():
            ad_serializer.save()
            return Response(ad_serializer.data, status=status.HTTP_201_CREATED)
        return Response(ad_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
