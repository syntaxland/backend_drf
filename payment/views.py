import random
import string
import requests

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
# from paystack.resource import TransactionResource
from app.models import Order
from payment.models import Payment
from .serializers import PaymentSerializer


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

        # Create the Payment instance
        payment = Payment.objects.create(
            user=user,
            reference=reference,
            amount=amount,
            order_id=order_id,
        )
        # Associate the payment with the corresponding order
        try:
            order = Order.objects.get(order_id=order_id)
            order.isPaid = True
            order.save()

            # payment.user_profile = UserProfile.objects.get_or_create(user=request.user)[0]

            payment.save()
            print('Payment details:', payment)
            # Return a success response
            return Response({'detail': 'Payment successful'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            pass
        serializer = PaymentSerializer(payment)
        return Response({'payment': serializer.data,}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
