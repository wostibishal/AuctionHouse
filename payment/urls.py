from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('checkout_session/<int:order_id>/', views.checkout_session, name='checkout_session'),
    path('ticket_session/<int:ticket_id>/', views.ticket_session, name='ticket_session'),
    path('Auction_session/<int:auction_id>/', views.Auction_session, name='Auction_session'),
    path('payment_success/',views.payment_success, name='payment_success'),
    path('ticket_payment_success/',views.ticket_payment_success, name='ticket_payment_success'),
    path('auction_payment_success/',views.auction_payment_success, name='auction_payment_success'),
    path('ticket_payment_cancel/',views.ticket_payment_cancel, name='ticket_payment_cancel'),
    path('auction_payment_cancel/',views.auction_payment_cancel, name='auction_payment_cancel'),
    path('payment_cancel/',views.payment_cancel, name='payment_cancel'),
]
