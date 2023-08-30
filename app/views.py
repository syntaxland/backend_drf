import random
import string
from django.db import IntegrityError

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import status, generics
from rest_framework.views import APIView
 
# from django.core import serializers
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache  
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User

from app.serializer import (ProductSerializer,  
                            OrderSerializer,
                            ShippingAddressSerializer,
                            OrderItemSerializer,
                            ReviewSerializer,
                            )
from app.models import Product, Order, OrderItem, ShippingAddress, Review
# from user_profile.models import UserProfile
from user_profile.serializers import UserSerializer


def generate_order_id():
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'ORD'+''.join(random.choices(letters_and_digits, k=7))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_id(request):
    order_id = generate_order_id()
    print('OrderID generated:', order_id)
    return Response({'order_id': order_id})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']
    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items.'}, status=status.HTTP_400_BAD_REQUEST)

    
    # Accessing the order_id 
    order_id = data.get('order_id')
    print('OrderID accessed:', order_id)
    if not order_id:
        return Response({'detail': 'Order ID not found.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create order
    order = Order.objects.create(
        user=user,
        paymentMethod=data['paymentMethod'],
        taxPrice=data['taxPrice'],
        shippingPrice=data['shippingPrice'],
        totalPrice=data['totalPrice'],
        order_id=order_id,
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_shipment(request):
    user = request.user
    data = request.data

    try:
        # Get the order by order_id
        order = get_object_or_404(Order, order_id=data['order_id'], user=user)

        # Create a new shipping address instance
        shipping_address = ShippingAddress.objects.create(
            user=user,
            order=order,
            address=data['address'],
            city=data['city'],
            postalCode=data['postalCode'],
            country=data['country'],
            shippingPrice=order.shippingPrice  
        )

        # Serialize the shipping address data for response
        serializer = ShippingAddressSerializer(shipping_address, many=False)
        
        return Response(serializer.data)

    except Exception as e:
        return Response({'detail': str(e)}, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_shipments(request):
    user = request.user
    try:
        shipments = ShippingAddress.objects.filter(user=user).order_by('-_id')
        serializer = ShippingAddressSerializer(shipments, many=True)
        return Response(serializer.data)
    except ShippingAddress.DoesNotExist:
            return Response({'detail': 'Shipping address not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
def get_all_user_shipments(request):
    try:
        shipments = ShippingAddress.objects.all().order_by('-_id')
        serializer = ShippingAddressSerializer(shipments, many=True)
        return Response(serializer.data)
    except ShippingAddress.DoesNotExist:
        return Response({'detail': 'Shipping address not found'}, status=status.HTTP_404_NOT_FOUND)
    
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def save_shipment(request):
#     user = request.user
#     data = request.data

#     # Assuming you have a serializer for ShippingAddress
#     serializer = ShippingAddressSerializer(data=data)
#     if serializer.is_valid():
#         # Set the user for the shipping address
#         serializer.save(user=user)
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors, status=400)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def save_shipment(request):
#     user = request.user
#     data = request.data
#     # order = ''

#     order_id = data.get('order_id')
#     if not order_id:
#         return Response({'detail': 'Order ID not found.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         order = Order.objects.get(order_id=order_id)
#     except ObjectDoesNotExist:
#         return Response({'detail': 'Order not found.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     serializer = ShippingAddressSerializer(data=data)
#     if serializer.is_valid():
#         address = serializer.validated_data['address']
#         city = serializer.validated_data['city']
#         postalCode = serializer.validated_data['postalCode']
#         country = serializer.validated_data['country']
#         shippingPrice = serializer.validated_data['shippingPrice']

#         ShippingAddress.objects.create(
#             order=order,
#             address=address,
#             city=city,
#             postalCode=postalCode,
#             country=country,
#             shippingPrice=shippingPrice
#         )
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-createdAt')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
def get_all_orders_view(request):
    try:
        orders = Order.objects.all().order_by('-createdAt')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_order(request, pk):
    user = request.user
    try:
        order = Order.objects.get(user=user, pk=pk)
        order.delete()
        return Response({'detail': 'Order deleted successfully.'})
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_items(request):
    user = request.user
    order_items = OrderItem.objects.filter(order__user=user).order_by('-_id')
    serializer = OrderItemSerializer(order_items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_shipping_address(request):
    user = request.user
    try:
        order_shipment = ShippingAddress.objects.filter(order__user=user)
        serializer = ShippingAddressSerializer(order_shipment, many=True)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except ShippingAddress.DoesNotExist:
        return Response({'detail': 'Shipment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def add_review(request):
    user = request.user
    if request.method == 'POST':
        order_item_id = request.data.get('order_item_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        print(order_item_id, rating, comment)

        order_item = get_object_or_404(OrderItem, _id=order_item_id)

        # Check if the logged-in user is the same user who created the order
        if user == order_item.order.user: 
            review = Review.objects.create(
                order_item=order_item,
                rating=rating,
                comment=comment,
                user=user,
                product=order_item.product,
                name=order_item.name, 
            )

            # # Update the numReviews field of the related product
            # product = order_item.product
            # product.numReviews = Review.objects.filter(product=product).count()
            # product.save()
            # Update the rating and numReviews fields of the related product
            product = order_item.product
            reviews = Review.objects.filter(product=product)
            product.numReviews = reviews.count()
            product.rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.save()
            
            serializer = ReviewSerializer(review, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'You are not authorized to add a review for this order item.'}, 
                            status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_review(request, review_id):
    user = request.user
    try:
        review = Review.objects.get(_id=review_id, user=user)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        rating = request.data.get('rating')
        comment = request.data.get('comment')

        # Check if the logged-in user is the same user who created the review
        if user == review.user:
            old_rating = review.rating  # Store the old rating for later adjustment
            review.rating = rating
            review.comment = comment
            review.save()

            # Update the rating and numReviews fields of the related product
            product = review.product
            reviews = Review.objects.filter(product=product)
            product.numReviews = reviews.count()
            product.rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.save()

            serializer = ReviewSerializer(review, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'You are not authorized to edit this review.'},
                            status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])  # Add this decorator to check if user is authenticated
# def edit_review(request, review_id):
#     user = request.user
#     try:
#         review = Review.objects.get(_id=review_id, user=user)
#     except Review.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         rating = request.data.get('rating')
#         comment = request.data.get('comment')

#         # Check if the logged-in user is the same user who created the review
#         # if request.user == review.order_item.order.user:
#         #     review.rating = rating
#         #     review.comment = comment
#         #     review.save()

#         #     serializer = ReviewSerializer(review, many=False)
#         #     return Response(serializer.data, status=status.HTTP_200_OK)
#         # else:
#         #     return Response({'detail': 'You are not authorized to edit this review.'},
#         #                     status=status.HTTP_403_FORBIDDEN)

#         # if user == review.order_item.order.user:
#         review.rating = rating
#         review.comment = comment
#         review.save()

#         serializer = ReviewSerializer(review, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#         # else:
#             # return Response({'detail': 'You are not authorized to edit this review.'},
#             #                 status=status.HTTP_403_FORBIDDEN)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def review_list_view(request, product_id):
    print('product_id:',product_id)
    try:
        review_list = Review.objects.filter(product_id=product_id).order_by('-createdAt')
        serializer = ReviewSerializer(review_list, many=True)
        return Response(serializer.data)
    except Review.DoesNotExist:
        return Response({'detail': 'Reviews not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_reviews(request):
    user = request.user
    try:
        order_reviews = Review.objects.filter(user=user).order_by('-createdAt')
        serializer = ReviewSerializer(order_reviews, many=True)
        return Response(serializer.data)
    except Review.DoesNotExist:
        return Response({'detail': 'Reviews not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def confirm_order_delivery(request, pk):
    user = request.user
    try:
        order = Order.objects.get(pk=pk, user=user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if order.isDelivered:
        order.isDelivered = True
        order.isDelivered.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET'])
def getRoutes(request):
    return Response('Welcome user!')

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

