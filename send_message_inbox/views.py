from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import status, generics
from rest_framework.views import APIView

from .serializers import SendMessageInboxSerializer   
from .models import  SendMessageInbox

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model() 


@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def send_message_to_all(request):
    if request.method == 'POST':
        subject = request.data.get('subject')
        message = request.data.get('message')

        if not subject or not message:
            return Response({'error': 'Subject and message are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        sender = request.user  
        receivers = User.objects.exclude(id=sender.id)      

        # Create messages for each receiver
        for receiver in receivers:
            inbox = SendMessageInbox.objects.create(
                sender=sender,
                receiver=receiver,
                subject=subject,
                message=message
            )

            serializer = SendMessageInboxSerializer(inbox, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'You are not authorized.'}, 
                            status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_inbox_view(request):
    try:
        message_inbox = SendMessageInbox.objects.all().order_by('-timestamp')
        serializer = SendMessageInboxSerializer(message_inbox, many=True)
        return Response(serializer.data)
    except SendMessageInbox.DoesNotExist:
        return Response({'detail': 'Messages not found'}, status=status.HTTP_404_NOT_FOUND)
    

# class SendMessageView(generics.ListCreateAPIView):
#     queryset = SendMessageInbox.objects.all()
#     serializer_class = SendMessageInboxSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(sender=self.request.user)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def message_inbox_view(request):
#     user = request.user
#     message_inbox = SendMessageInbox.objects.filter(receiver=user).order_by('-timestamp')
#     serializer = SendMessageInboxSerializer(message_inbox, many=True)
#     return Response(serializer.data)





# @api_view(['POST'])
# @permission_classes([IsAuthenticated])  
# def send_message_inbox_view(request):
#     user = request.user
#     data = request.data
    # data['user'] = user.id 

    # serializer = CreditPointRequestSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response({'success': 'Credit point request submitted successfully.'})
    # return Response(serializer.errors, status=400)


