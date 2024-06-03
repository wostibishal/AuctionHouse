from django.shortcuts import render, redirect, get_object_or_404
from order.models import Order, OrderItem
from cart.models import CartItem
from .models import Payment
from ticket.models import Ticket
from auctions.models import Auction
from django.contrib import messages
import stripe
# Create your views here.
stripe.api_key = 'sk_test_51Oyt6l2LEh1iI45eunNKl7NZd7XVLtwGdcF8wZOhcr6NiFojxcQG90ojfCZw35uabcheyzRwGbCCqtUZD5BEK6Ec000BiKUUZk'
def checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id, is_completed=True)
    orderitems = get_object_or_404(OrderItem, order=order)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'npr',  
                    'product_data': {
                        'name': f'Order {order.id} Payment'
                    },
                    'unit_amount': int(order.total_price*100),  
                },
                'quantity': orderitems.quantity,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('http://127.0.0.1:8000/payment/payment_success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('http://127.0.0.1:8000/payment/payment_cancel/'),
            client_reference_id=str(order.id)
        )
        return redirect(session.url, code=303)
    
    except Exception as e:
        messages.error(request, f"Error processing payment: {str(e)}")
        return redirect('index')

def ticket_session(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'npr',  
                    'product_data': {
                        'name': f'Order {ticket.id} Payment'
                    },
                    'unit_amount': int(ticket.price*100),  
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('http://127.0.0.1:8000/payment/ticket_payment_success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('http://127.0.0.1:8000/payment/ticket_payment_cancel/'),
            client_reference_id=str(ticket.id)
        )
        return redirect(session.url, code=303)
    except Exception as e:
        messages.error(request, f"Error processing payment: {str(e)}")
        return redirect('index')
    
def Auction_session(request, auction_id):
    Auctions = get_object_or_404(Auction, pk=auction_id)
    print (Auctions)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'npr',  
                    'product_data': {
                        'name': f'Order {Auctions.id} Payment'
                    },
                    'unit_amount': int(Auctions.current_bid*100),  
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('http://127.0.0.1:8000/payment/auction_payment_success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('http://127.0.0.1:8000/payment/auction_payment_cancel/'),
            client_reference_id=str(Auctions.id)
        )
        return redirect(session.url, code=303)
    except Exception as e:
        messages.error(request, f"Error processing payment: {str(e)}")
        return redirect('index')

def ticket_payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "No session ID found.")
        return redirect('index')
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        ticket_id = session.client_reference_id
        ticket = Ticket.objects.get(pk=ticket_id)
        Payment.objects.create(
            ticket= ticket,
            user=request.user,
            paid_amount=ticket.price,
            stripe_charge_id=session.payment_intent,
        )
        messages.success(request, 'Payment successful')
        return redirect('ticket:purchase_ticket', ticket_id=ticket_id)
    except stripe.error.StripeError as e:
        messages.error(request, f"Stripe error: {str(e)}")
        return redirect('index')
    except Ticket.DoesNotExist:
        messages.error(request, "ticket not found.")
        return redirect('index')
    except Exception as e:
        messages.error(request, f"Error processing payment: {str(e)}")
        return redirect('index')
    
def auction_payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "No session ID found.")
        return redirect('index')
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        auction_id = session.client_reference_id
        auction = Auction.objects.get(pk=auction_id)
        Payment.objects.create(
            auction=auction,
            user=request.user,
            paid_amount=auction.current_bid,
            stripe_charge_id=session.payment_intent,
        )
        messages.success(request, 'Payment successful')
        return redirect('index')
    except stripe.error.StripeError as e:
        messages.error(request, f"Stripe error: {str(e)}")
        return redirect('index')
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('index')
    except Exception as e:
        messages.error(request, f"Error processing payment: {str(e)}")
        return redirect('index')
    
def payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "No session ID found.")
        return redirect('index')
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        order_id = session.client_reference_id
        order = Order.objects.get(pk=order_id)
        Payment.objects.create(
            order=order,
            user=request.user,
            paid_amount=order.total_price,
            stripe_charge_id=session.payment_intent,
        )
        messages.success(request, 'Payment successful')
        return redirect('index')
    except stripe.error.StripeError as e:
        messages.error(request, f"Stripe error: {str(e)}")
        return redirect('index')
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('index')
    except Exception as e:
        messages.error(request, f"Error processing payment: {str(e)}")
        return redirect('index')

def auction_payment_cancel(request):
    messages.error(request, 'payment cancelled')
    return redirect ('index')

def ticket_payment_cancel(request):
    messages.error(request, 'payment cancelled')
    return redirect ('index')

def payment_cancel(request):
    messages.error(request, 'payment cancelled')
    return redirect ('index')
