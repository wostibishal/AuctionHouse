
from django.shortcuts import get_object_or_404, redirect, render
from .form import  AuctionItemUpdateForm, AuctionItemForm, AuctionForm, UpdateAuctionForm
from django.contrib import messages
from ticket.models import Ticket, TicketPurchaseList
from .models import AuctionItem, Auction,Bid
from chat.models import ChatRoom, ChatMessage
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

# Create your views here.

def AuctionItem_detail(request, pk):
    auction_item = get_object_or_404(AuctionItem, pk=pk)
    return render(request,'auction/auction_item_details.html',{
        'auction_item': auction_item
    })

def auction_list(request):
    auction = Auction.objects.all()
    if not auction:
        messages.info(request, 'There are no auctions available.')
        return redirect('index')
    return render(request, 'auction/auction_list.html', {
        'auction': auction,
    })

def my_auction_list(request):
    my_auction = Auction.objects.filter(item__user=request.user)
    if not my_auction:
        messages.info(request, 'you have no auction.')
        return redirect('index')
    return render(request, 'auction/my_auction_list.html', {
        'auction': my_auction,
    })
@csrf_protect
def add_AuctionItems(request):
    if request.method == 'POST':
        form = AuctionItemForm (request.POST, request.FILES)
        if form.is_valid():
            AuctionItem =form.save(commit=False)
            AuctionItem.user = request.user
            form.save()
            messages.success(request, 'auction item is created')
            return redirect('index')
        else:
            messages.error(request,'there was something wrong')
    else:
        form = AuctionItemForm()
        
    return render(request, 'auction/add_auction_product.html', {
        'form': form,
    })
@csrf_protect
def update_AuctionItem(request, pk):   
    auction_item = get_object_or_404(AuctionItem, pk=pk)  
    if request.method == 'POST':
        form = AuctionItemUpdateForm(request.POST, request.FILES, instance=auction_item)
        if auction_item.user == request.user:
            if form.is_valid():
                form.save()
                messages.success(request, 'auction updated')
                return redirect('auctions:AuctionItem_detail', pk=pk)  
            else:
                messages.error(request, 'There was something wrong')
        else:
            messages.error(request,'you are not authorized to update this item')
    else:
        form = AuctionItemUpdateForm(instance=auction_item)
    
    return render(request, 'auction/auction_item_update.html', {
        'form': form, 
        'auction_item': auction_item,
    })
@csrf_protect
def delete_AuctionItem(request, pk):
    item = get_object_or_404(AuctionItem, pk=pk)
    if item.user == request.user:
        if request.method == "POST":  
            item.delete()
            messages.success(request, 'Item deleted')
            return redirect('index')  
    else:
        messages.error(request, 'You are not authorized to delete this item')
    return render(request,'auction/AuctionItem_details.html')
@csrf_protect
def go_to_auction(request, pk ):
    auction = get_object_or_404(Auction, pk=pk)
    if auction.is_sold == False:
        messages.error(request,'this item is no longer in auction ')
        return redirect('index')
@csrf_protect
def create_auction(request, pk):
    item = get_object_or_404(AuctionItem, pk=pk)
    now = timezone.now()
    if request.method == 'POST':
        form = AuctionForm (request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.item = item
            auction.save()
            messages.success(request, 'auction is created')
            return redirect('index')
        else:
            messages.error(request,'there was something wrong')
    else:
        form = AuctionForm()
        
    return render(request, 'auction/create_auction.html', {
        'form': form,
    })
@csrf_protect
def auction_update(request, auction_id):   
    auction = get_object_or_404(Auction, pk=auction_id)  
    if request.method == 'POST':
        form = UpdateAuctionForm(request.POST, request.FILES, instance = auction)
        if auction.item.user == request.user:
            if form.is_valid():
                form.save()
                messages.success(request, 'auction updated')
                return redirect('auctions:my_auction_list')  
            else:
                messages.error(request, 'There was something wrong')
        else:
            messages.error(request,'you are not authorized to update this item')
    else:
        form = UpdateAuctionForm(instance=auction)
    
    return render(request, 'auction/auction_update.html', {
        'form': form, 
        'auction': auction,
        'auction_id':auction_id,
    })
@csrf_protect
def auction_delete(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    if auction.item.user == request.user:
        if request.method == "POST":  
            auction.delete()
            messages.success(request, 'Item deleted')
            return redirect('index')  
    else:
        messages.error(request, 'You are not authorized to delete this item')
    return render(request,'index.html')


@csrf_protect
def auction_bid(request, auction_id):
    user = request.user
    auction = get_object_or_404(Auction, pk=auction_id)
    latest_bid = Bid.objects.filter(auction=auction).order_by('-timestamp').first()
    ticket = Ticket.objects.filter(title = auction)
    room, created = ChatRoom.objects.get_or_create(auction=auction)
    chat_messages = ChatMessage.objects.filter(room=room)
    now = timezone.now()
    if request.method == 'POST' and user.is_authenticated:
        bid_amount = request.POST.get('bid_amount')
        try:
            bid_amount = float(bid_amount)
        except ValueError:
            messages.error(request, "Invalid bid amount.")
            return redirect('auctions:auction_bid', pk=auction_id)
        ticket_list = TicketPurchaseList.objects.filter(user=user, ticket=ticket)
        if not ticket_list.exists():
            messages.error(request, "You don't have tickets to bid on this auction.")
            return redirect('ticket:list_ticket')

        if bid_amount <= auction.current_bid:
            messages.error(request, "Your bid must be higher than the current bid.")
            return redirect('auctions:auction_bid', pk=auction_id)
        # Process the valid bid
        Bid.objects.create(user=user, auction=auction, bid_amount=bid_amount)
        auction.current_bid = bid_amount
        auction.save()
        messages.success(request, "Your bid has been placed successfully.")
        return redirect('auctions:auction_bid', pk=auction_id)
    context = {
        'auction': auction,
        'latest_bid': latest_bid,
        'user': user,
        'room': room,
        'now': now,
        'chat_messages': chat_messages,
        'auction_id': auction_id
    }
    return render(request, 'auction/auction_bid.html', context)