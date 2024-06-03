from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .form import AddItemForm, UpdateItemForm, ReviewForm
from .models import Category, Item, Review
from order.models import Order, OrderItem
from user.models import SellerProfile
from django.db.models import Avg
from django.contrib.auth.decorators import login_required


# Create your views here.
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item/item_list.html', {'items': items})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user = request.user
    if user == None:
        return redirect ('item_detail')
    order_item = None
    try:
        order_item = OrderItem.objects.get(item=item)  # Correctly access OrderItem
        order = order_item.order  # Assuming OrderItem has a foreign key to Order
    except OrderItem.DoesNotExist:
        order = None
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:6]
    reviews = Review.objects.filter(item=item)
    average_rating = None
    if reviews.exists():
        average_rating = reviews.aggregate(average=Avg('rating'))['average']
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully.')
            return redirect('index')  
        else:
            messages.error(request, 'There was an error adding the review.')
    return render(request, 'item/item_detail.html', {
        'item': item,
        'related_items': related_items,
        'reviews': reviews,
        'average_rating': average_rating,
        'order': order,
        'order_item': order_item,
        'form': form,
    })

def item_add(request):
    try:
        seller_profile = request.user.sellerprofile
    except SellerProfile.DoesNotExist:
        seller_profile = None
    if seller_profile:
        if request.method == 'POST':
            form = AddItemForm(request.POST, request.FILES)
            if form.is_valid():
                item = form.save(commit=False)
                item.market_name = seller_profile
                item.save()
                messages.success(request, 'Item added successfully.')
                return redirect('index')  
            else:
                messages.error(request, 'There was an error adding the item.')
        else:
            form = AddItemForm(initial={'market_name': seller_profile})
    else:
        messages.error(request, 'You are not authorized to add items.')
        return redirect('index') 

    return render(request, 'item/item_add.html', {'form': form})




def item_update(request, pk):   
    seller_profile = request.user.sellerprofile
    item = get_object_or_404(Item, pk=pk) 
    if seller_profile:
        if request.method == 'POST':
            form = UpdateItemForm(request.POST, request.FILES, instance=item) 
            if form.is_valid():
                form.save()
                messages.success(request, 'Item updated')
                return redirect('item:item_detail', pk=pk)  
            else:
                messages.error(request, 'There was something wrong')
        else:
            form = UpdateItemForm(instance=item)
    elif request.user.is_superuser:
        if request.method == 'POST':
            form = UpdateItemForm(request.POST, request.FILES, instance=item)  
            if form.is_valid():
                form.save()
                messages.success(request, 'Item updated')
                return redirect('item:item_detail', pk=pk)  
            else:
                messages.error(request, 'There was something wrong')
        else:
            form = UpdateItemForm(instance=item)
    else:
        messages.error(request, 'You are not authorized to perform this action')
        return redirect('item:item_detail', pk=pk)
    return render(request, 'item/item_update.html', {
        'form': form, 
        'item': item,
    })

def item_delete(request, pk):
    seller_profile = request.user.sellerprofile
    item = get_object_or_404(Item, pk=pk)
    if seller_profile:    
        if request.method == 'POST':
                item.delete()
                messages.success(request, 'Item deleted') 
        else:
            messages.error(request, 'something went wrong.')
    elif request.user.is_superuser:
        if request.method == 'POST': 
                item.delete()
                messages.success(request, 'Item deleted') 
        else:
            messages.error(request, 'something went wrong.')
    return redirect('index')


# def purchase_item(request, pk):
#     messages.success(request, 'Item purchased successfully!')
#     return redirect('item:detail', pk=pk)


