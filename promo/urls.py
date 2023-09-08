from django.urls import path
from . import views

urlpatterns = [
    path("apply-promo/", views.apply_promo_code, name="apply-promo-code"),
    path("refer/", views.refer_user, name="refer-user"),
]
