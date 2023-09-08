from django.urls import path
from . import consumers
from . import views

urlpatterns = [
    # Define a URL pattern for WebSocket chat room
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),

    # Define API endpoints for sending and retrieving chat messages
    path('chat/<str:room_id>/messages/', views.get_messages, name='get_messages'),
    path('chat/<str:room_id>/send/', views.send_message, name='send_message'),

    # Add other chat-related views and URLs as needed
]
