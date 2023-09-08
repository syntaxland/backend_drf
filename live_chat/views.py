from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, room_id):
    try:
        messages = ChatMessage.objects.filter(room__id=room_id)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, room_id):
    try:
        user = request.user
        content = request.data.get('content', '')

        if not content:
            return Response({'error': 'Content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        room = ChatRoom.objects.get(id=room_id)
        message = ChatMessage.objects.create(room=room, user=user, content=content)

        serializer = ChatMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Message, ChatRoom
# from .serializers import MessageSerializer

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def send_message(request):
#     user = request.user
#     room_id = request.data.get('room_id')
#     content = request.data.get('content')

#     try:
#         room = ChatRoom.objects.get(id=room_id)
#     except ChatRoom.DoesNotExist:
#         return Response({'error': 'Chat room does not exist.'}, status=400)

#     message = Message.objects.create(room=room, sender=user, content=content)

#     # Send the message to the appropriate room using Channels
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         str(room.id),
#         {
#             'type': 'chat.message',
#             'message': MessageSerializer(message).data,
#         }
#     )

#     return Response({'message': 'Message sent successfully.'})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_messages(request, room_id):
#     try:
#         room = ChatRoom.objects.get(id=room_id)
#     except ChatRoom.DoesNotExist:
#         return Response({'error': 'Chat room does not exist.'}, status=400)

#     messages = Message.objects.filter(room=room).order_by('timestamp')
#     serializer = MessageSerializer(messages, many=True)

#     return Response({'messages': serializer.data})
