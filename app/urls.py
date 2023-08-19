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

    path('get-user-orders/', views.get_user_orders, name='get-user-orders'),
    path('delete-orders/<int:pk>/', views.delete_user_order, name='delete-order'),

    

    # path('get-user-order-item/', views.get_user_order_item, name='get-user-orders-item'),

    # path('api/products/<str:product_id>/add-review/', views.add_review, name='add-review'),


    # path('get-user-order-reviews/', views.OrderReviews, name='get-reviews'),
    # path('create-user-order-review/', views.OrderReviews, name='create-review'),
    # path('edit-user-order-review/', views.OrderReviews, name='edit-reviews'),

    path('order/<int:order_id>/items/', views.get_order_items, name='order-items'),
    path('products/<int:product_id>/reviews/', views.add_review, name='add-review'),
    path('order/<int:order_id>/confirm-delivery/', views.confirm_delivery, name='confirm-delivery'),

    # path('delete-orders/<int:pk>/', views.delete_order, name='delete-order'),
]
