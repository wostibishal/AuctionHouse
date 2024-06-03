from django.shortcuts import render, redirect, get_object_or_404
from item.models import Item
from order.models import Order
from .models import CartItem, Cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@login_required
@csrf_protect
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        item.quantity -= 1
    return redirect('index')  

@csrf_protect
@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, pk=pk)
    cart_item.delete()
    item.quantity += cart_item.quantity 
    return redirect('cart:view_cart') 

@login_required
def view_cart(request):
    user = request.user
    cart, created= Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('item')
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    has_order = Order.objects.filter(user=user, is_completed=True).exists()
    if not created:
        return render(request,'cart/view_cart.html',{'cart_items': cart_items,
        'total_price': total_price,
        'user_has_order': has_order}) 
        
    return render(request, 'cart/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'user_has_order': has_order 
    })