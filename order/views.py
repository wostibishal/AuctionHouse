from django.shortcuts import redirect, render, get_object_or_404

from item.models import Item
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages


@login_required
def save_orders(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    order_items_list = []
    with transaction.atomic():
        order, created = Order.objects.get_or_create(user=user, is_completed=False)
        if created or not order.orderitem_set.exists():  # Check if order items already exist for this order
            total_price = 0
            for cart_item in cart_items:
                total_price += cart_item.item.price * cart_item.quantity
                order_items = OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    quantity=cart_item.quantity,
                    price=cart_item.item.price
                )
                order_items_list.append(order_items)
                cart_item.delete()

            order.total_price = total_price
            order.is_completed = True  # Mark the order as completed
            order.save()
            messages.success(request, f'Order {order.id} saved successfully!')
            # return redirect('order:save_order', order_id=order.id)

    return render(request,'order/save_orders.html', {
        'cart': cart,
        'cart_items': cart_items,
        'order': order,
        'order_items_list': order_items_list,
})
