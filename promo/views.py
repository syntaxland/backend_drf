from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PromoCode, Referral
from .serializers import PromoCodeSerializer, ReferralSerializer
from django.utils import timezone


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_promo_code(request):
    promo_code = request.data.get("promo_code")
    try:
        promo = PromoCode.objects.get(code=promo_code, expiration_date__gte=timezone.now())
        return Response({
            "message": "Promo code applied successfully",
            "discount_percentage": promo.discount_percentage,
            "expiration_date": promo.expiration_date
        })
    except PromoCode.DoesNotExist:
        return Response({"error": "Invalid promo code or expired"}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def refer_user(request):
    referral_code = request.data.get("referral_code")
    referred_by = request.user
    try:
        referral = Referral.objects.get(referral_code=referral_code)
        referral.referred_by = referred_by
        referral.save()
        return Response({"message": "User referred successfully"})
    except Referral.DoesNotExist:
        return Response({"error": "Referral code not found"}, status=400)
