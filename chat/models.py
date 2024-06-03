from django.db import models
from user.models import User
from auctions.models import Auction
# Create your models here.
class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='chat_rooms')

    def __str__(self):
        return f"Chat Room for {self.auction.title}"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name}: {self.message[:50]}'
