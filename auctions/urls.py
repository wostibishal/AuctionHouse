from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'auctions'

urlpatterns = [
    path ('<int:pk>/auction_item_details/', views.AuctionItem_detail, name='AuctionItem_detail'),
    path ('add_auction_product/',views.add_AuctionItems,name='add_auction_product'),
    path ('<int:pk>/auction_item_update/', views.update_AuctionItem, name='AuctionItem_update'),
    path ('<int:pk>/auction_item_delete/', views.delete_AuctionItem, name='AuctionItem_delete'),
    path ('auction_list/', views.auction_list ,name='auction_list'),
    path ('my_auction_list/', views.my_auction_list ,name='my_auction_list'),
    path ('<int:pk>/create_auction/', views.create_auction,name='create_auction'),
    path ('<int:auction_id>/auction_update/', views.auction_update,name='auction_update'),
    path ('<int:pk>/auction_delete/', views.auction_delete,name='auction_delete'),
    path ('<int:auction_id>/go_to_auction/', views.go_to_auction,name='go_to_auction'),
    path('<int:auction_id>/auction_bid/', views.auction_bid, name='auction_bid'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)