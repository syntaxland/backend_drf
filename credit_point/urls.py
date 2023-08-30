from django.urls import path
from . import views

urlpatterns = [
    path('credit-point-request/', views.credit_point_request_view, name='credit_point_request'),
    path('get-all-credit-points/', views.get_all_credit_points_view, name='get-all-credit-points'),
    path('get-credit-point/', views.get_user_credit_point_view, name='get-credit-point'),

]
