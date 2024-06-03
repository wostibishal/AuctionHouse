from django.utils import timezone
from django.db import models
from user.models import User 

class Auction_category(models.Model):
    Category = models.CharField(max_length=100, null=True, blank=True) 
    
    def clean(self):
        self.Category = self.Category.capitalize()
    def __str__(self):
        return self.Category
    
class AuctionItem(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Auction_category, on_delete=models.PROTECT, default=None, blank=True, null= True)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='auction_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.item_name

class Auction(models.Model): 
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100, default=None)
    starting_time =models.DateTimeField(default =timezone.now)
    end_time = models.DateTimeField()
    start_price = models.FloatField(default=0) 
    is_sold = models.BooleanField(default=False)
    current_bid = models.FloatField(default=0)

    def __str__(self):
        return self.title

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_amount = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.bid_amount)+" "+str(self.auction)

class AuctionPurchase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email