import random
import string
import requests
from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.http import Http404
from django.db.models import Sum

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
# from paystack.resource import TransactionResource
from app.models import Product, Order, OrderItem, ShippingAddress
from payment.models import Payment
from .serializers import PaymentSerializer, UserPaymentSerializer
from credit_point.models import CreditPoint

def generate_payment_reference():
    return ''.join(random.choices(string.digits, k=10))


class PaymentDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        public_key = settings.PAYSTACK_PUBLIC_KEY
        # email = request.user.email
        reference = generate_payment_reference()
        print(public_key, reference)
        # print(public_key, reference, email)
        return Response({"publicKey": public_key,
                             "reference": reference,
                            #  "email": email,
                             })
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    user = request.user
    data = request.data
    try:
        amount = int(request.data.get('amount'))
        # email = user.email
        email = request.data.get('email')
        reference = data.get('reference')
        order_id = data.get('order_id')
        print('Payment Details:','Amount:', amount,'Reference:', 
              reference, 'Order ID:', order_id, 'Email:', email)
        if not order_id:
            return Response({'detail': 'Order ID not found.'}, status=status.HTTP_400_BAD_REQUEST)

        
        # Associate the payment with the corresponding order
        try:
            order = Order.objects.get(order_id=order_id)
            # order = Order.objects.get(order_id=order_id)

            # Create the Payment instance
            payment = Payment.objects.create(
                user=user,
                reference=reference,
                amount=amount,
                order=order,
            )

            order.isPaid = True
            order.paidAt = payment.created_at
            order.save()

            payment.save()
            print('Payment details:', payment)

            # Calculate the credit points earned (1% of payment amount)
            # credit_points_earned = amount * 0.01
            credit_points_earned = Decimal(str(amount)) * Decimal('0.01')

            try:
                # Get or create the user's credit point balance
                credit_point, created = CreditPoint.objects.get_or_create(
                    user=request.user,
                    # credit_points_earned=credit_points_earned
                    )
                # credit_point = CreditPoint.objects.create(
                #     user=request.user,
                #     )
                credit_point.balance += credit_points_earned
                credit_point.save()
                print('Credit points added:', credit_point, credit_points_earned)
                return Response({'detail': 'Credit points added.'}, status=status.HTTP_201_CREATED)
            except CreditPoint.DoesNotExist:
                pass

            # Return a success response
            return Response({'detail': 'Payment successful'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            pass
        serializer = PaymentSerializer(payment)
        return Response({'payment': serializer.data,}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_payments(request):
    user = request.user
    payments = Payment.objects.filter(user=user).order_by('-created_at')
    serializer = UserPaymentSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated]) 
def get_all_payments_view(request):
    try:
        all_payments = Payment.objects.all().order_by('-created_at')
        serializer = PaymentSerializer(all_payments, many=True)
        return Response(serializer.data)
    except Payment.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_payments(request):
#     payments = Payment.objects.all().order_by('-created_at')
#     serializer = PaymentSerializer(payments, many=True)
#     return Response(serializer.data)

 
# @api_view(['GET'])
# # @permission_classes([IsAdminUser])
# @permission_classes([IsAuthenticated])
# def get_all_payments(request):
#     payments = Payment.objects.values('user__username').annotate(total=Sum('amount')).order_by('user')
#     return Response(payments)
  

