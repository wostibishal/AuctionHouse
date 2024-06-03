from django.db import models
from auctions.models import Auction 
from user.models import User

# Create your models here.
class Ticket(models.Model):
    title = models.OneToOneField(Auction, on_delete=models.CASCADE, default=None, unique=True)
    price = models.FloatField(default=0)
    description = models.TextField(blank=True, null=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket for Auction: {self.title.title}, Price: {self.price}"
    
class TicketPurchaseList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return str(self.user.first_name) + " ticket " + str(self.ticket.title) 