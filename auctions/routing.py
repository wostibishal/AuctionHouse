# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/auctions/(?P<auction_id>\d+)/auction_bid/$', consumers.UnifiedAuctionChatConsumer.as_asgi()),
]