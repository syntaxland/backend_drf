from django.urls import path
from . import views

urlpatterns = [
    path('get-payment-details/', views.PaymentDetailsView.as_view(), name='get_payment_details'),
    path('create-payment/', views.create_payment, name='create_payment'),
]
