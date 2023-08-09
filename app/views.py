import random
import string

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import status, generics
from rest_framework.views import APIView

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache  

from app.serializer import (ProductSerializer, 
                            UserSerializer, 
                            UserSerializerWithToken, 
                            OrderSerializer)
from app.models import Product, Order, OrderItem, ShippingAddress
# from user_profile.models import UserProfile

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfiles(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
def getUsers(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

def generate_order_id():
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'ORD'+''.join(random.choices(letters_and_digits, k=7))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_id(request):
    order_id = generate_order_id()
    print('OrderID generated:', order_id)
    return Response({'order_id': order_id})


# @csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']
    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)

    shippingAddress = data.get('shippingAddress', {})  # Get shipping address object or empty dict

    # Accessing the order_id 
    order_id = data.get('order_id')
    print('OrderID accessed:', order_id)
    if not order_id:
        return Response({'detail': 'Order ID not found.'}, 
                        status=status.HTTP_400_BAD_REQUEST)

    # Create order
    order = Order.objects.create(
        user=user,
        paymentMethod=data['paymentMethod'],
        taxPrice=data['taxPrice'],
        shippingPrice=data['shippingPrice'],
        totalPrice=data['totalPrice'],
        order_id=order_id,
    )

    # order.user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    # order.save()

    # Create shipping address if it exists
    if shippingAddress:
        ShippingAddress.objects.create(
            order=order,
            address=shippingAddress.get('address', ''),
            city=shippingAddress.get('city', ''),
            postalCode=shippingAddress.get('postalCode', ''),
            country=shippingAddress.get('country', ''),
            shippingPrice=data['shippingPrice'],
        )

    # Create order items
    for item in orderItems:
        product = Product.objects.get(_id=item['product'])

        OrderItem.objects.create(
            product=product,
            order=order,
            name=product.name,
            qty=item['qty'],
            price=item['price'],
            image=product.image.url,
        )

    # Serialize the order and add order_id to the serialized data
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not authorized to view this order'}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getRoutes(request):
    return Response('Welcome user!')
 

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)
 

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk):
        if pk == 'search':  # Handle search case
            queryset = self.get_queryset()
            keyword = self.request.query_params.get('search', None)
            if keyword:
                queryset = queryset.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response([])
        else:
            product = get_object_or_404(self.get_queryset(), _id=pk)
            serializer = self.get_serializer(product)
            return Response(serializer.data) 

class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get('search', None)
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
        return queryset



# # Registering the new users
# @api_view(['POST'])
# def registerUser(request):
#     data = request.data
#     print(data)
#     try:
#         user = User.objects.create(
#             first_name=data['name'],
#             username=data['email'],
#             email=data['email'],
#             password=make_password(data['password'])
#         )
#         serializer = UserSerializerWithToken(user, many=False)
#         return Response(serializer.data)
#     except:
#         message = {'details': 'Bad request: User already exist or null.'}
#         return Response(message, status=status.HTTP_400_BAD_REQUEST)

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

#     def validate(self, attrs):
#         data = super().validate(attrs)
#         serializer = UserSerializerWithToken(self.user).data
#         for k, v in serializer.items():
#             data[k] = v
#         return data


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer



# @api_view(['GET'])
# def searchProducts(request):
#     query = request.query_params.get('q')
#     if query:
#         products = Product.objects.filter(
#             Q(name__icontains=query) | Q(description__icontains=query)
#         )
#     else:
#         products = Product.objects.all() 
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def searchProducts(request):
#     query = request.data.get('q')

#     if query:
#         products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({"products": []})
