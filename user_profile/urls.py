from django.urls import path
from . import views

urlpatterns = [
    path('users/register/', views.register_user_view, name='user-register'),
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/logout/', views.LogoutView.as_view(), name='user-logout'),
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('user-account-delete/', views.UserAccountDeleteView.as_view(), name='user-account-delete'),
    # path('toggle-favorite/<int:product_id>/', views.toggle_favorite),
]
