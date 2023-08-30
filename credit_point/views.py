from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import status, generics
from rest_framework.views import APIView
 
# from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache  
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# from django.contrib.auth.models import User

from .serializer import CreditPointRequestSerializer  
from .models import  CreditPointRequest

from django.contrib.auth import get_user_model

User = get_user_model() 


@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def credit_point_request_view(request):
    user = request.user
    data = request.data
    data['user'] = user.id 

    serializer = CreditPointRequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'Credit point request submitted successfully.'})
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_credit_point_view(request):
    user = request.user
    try:
        credit_point = CreditPointRequest.objects.filter(user=user).order_by('-created_at')
        serializer = CreditPointRequestSerializer(credit_point, many=True)
        return Response(serializer.data)
    except CreditPointRequest.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
def get_all_credit_points_view(request):
    try:
        all_credit_points = CreditPointRequest.objects.all().order_by('-created_at')
        serializer = CreditPointRequestSerializer(all_credit_points, many=True)
        return Response(serializer.data)
    except CreditPointRequest.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])  
# def credit_point_request_view(request):
#     user = request.user
#     data = request.data
#     data['user'] = user.id  # Set the user to the current user

#     try:
#         credit_point_request = CreditPointRequest.objects.create(**data)
#         return Response({'success': 'Credit point request submitted successfully.'})
#     except IntegrityError as e:
#         return Response({'error': 'An error occurred while submitting the request.'}, status=400)
