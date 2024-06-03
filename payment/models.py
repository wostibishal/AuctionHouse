from django.db import models
from order.models import Order
from user.models import User
from ticket.models import Ticket
from auctions.models import Auction

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True, blank=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE,null=True, blank=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE,null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=50)  

    def __str__(self):
        detail = "No Order/Ticket/Auction"
        if self.order:
            detail = f"Order {self.order.id}"
        elif self.ticket:
            detail = f"Ticket {self.ticket.id}"
        elif self.auction:
            detail = f"Auction {self.auction.id}"
        return f"Payment {self.id} for {detail}"