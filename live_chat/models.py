# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model() 


# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     text = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

# class ChatRoom(models.Model):
#     participants = models.ManyToManyField(User, related_name='chat_rooms')
#     messages = models.ManyToManyField(Message)


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.content}'
 