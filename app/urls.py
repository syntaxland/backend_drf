from django.urls import path
from . import views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
# )

urlpatterns = [
    # path('/',views.index,name="index"),
    path('', views.getRoutes, name='getRouters'),
    # path('users/register/', views.registerUser, name='register'),
    # path('users/login/', views.LoginView.as_view(), name='token_obtain_pair'),
    # path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('products/', views.getProducts, name='getProducts'),
    path('products/<str:pk>/', views.ProductDetailView.as_view(), name='getProduct'),
    path('user/profile/', views.getUserProfiles, name="getUserProfiles"), 
    # path('products/<str:pk>/', views.getProduct, name='getProduct'),
    path('users/', views.getUsers, name="getUsers"),

    path('products/search/', views.ProductSearchView.as_view(), name='product-search'),
    path('create-order/', views.create_order, name='create_order'), 
    path('get-order-id/', views.get_order_id, name='get_order_id'),
]
