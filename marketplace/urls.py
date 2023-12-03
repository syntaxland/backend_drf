# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-marketplace-seller/', views.create_marketplace_seller, name='create-marketplace-seller'),
    path('marketplace-seller-photo/', views.create_marketplace_seller_photo, name='marketplace-seller-photo'),
    path('create-free-ad/', views.create_free_ad, name='create-free-ad'),
    path('create-paid-ad/', views.create_paid_ad, name='create-paid-ad'),

    path('get-marketplace-seller-account/', views.get_marketplace_seller_account, name='get-marketplace-seller-account'),
    path('update-marketplace-seller-account/', views.update_marketplace_seller_account, name='update-marketplace-seller-account'),

    path('get-marketplace-seller-photo/', views.get_marketplace_seller_photo, name='get_marketplace-seller-photo'),
    path('update-marketplace-seller-photo/', views.update_marketplace_seller_photo, name='update-marketplace-seller-photo'),

    path('get-seller-free-ad/', views.get_seller_free_ad, name='get-seller-free-ad'),
    path('update-seller-free-ad/<int:pk>/', views.update_seller_free_ad, name='update-seller-free-ad'),

    path('get-all-free-ad/', views.get_all_free_ad, name='get-all-free-ad'),

]
