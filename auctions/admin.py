from django.contrib import admin
from .models import  Auction, Bid, AuctionItem, Auction_category
# Register your models here.

class AuctionItemAdmin(admin.ModelAdmin):
    def __str__(self):
        return str(self.name) if self.name else f"AuctionItem {self.id}"


admin.site.register(Auction)
admin.site.register(Auction_category)
admin.site.register(Bid)
admin.site.register(AuctionItem, AuctionItemAdmin)