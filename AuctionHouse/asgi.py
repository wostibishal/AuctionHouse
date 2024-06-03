import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import auctions.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuctionHouse.settings')
Auction_websocket_urlpatterns = auctions.routing.websocket_urlpatterns
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(Auction_websocket_urlpatterns))),
})
