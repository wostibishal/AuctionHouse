from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count, Sum
from user.models import User, CustomerProfile, SellerProfile
from item.models import Category, Item
from auctions.models import AuctionItem, Auction
from ticket.models import Ticket, TicketPurchaseList
from payment.models import Payment
from django.contrib import messages, auth
from .forms import UserForm, SellerForm, CustomerProfileForm, UserInfoForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required 
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

# Create your views here.
def check_user_role(user, role):
    return user.is_authenticated and user.role == role

def detect_user_redirect_url(user):
    if user.role == User.SELLER:
        return 'seller_dashboard'
    elif user.role == User.CUSTOMER:
        return 'customer_dashboard'
    elif user.is_superuser:
        return '/admin'
    return 'index'

def index(request):
    categories = Category.objects.annotate(num_items=Count('items'))
    items = Item.objects.filter(is_sold=False)[:10]  
    auction_items = AuctionItem.objects.filter(is_sold=False)[:10]  
    
    if request.user.is_authenticated:
        if request.user.role == User.SELLER:
            seller_profile = request.user.sellerprofile
            items = Item.objects.filter(market_name=seller_profile, is_sold=False)[:20]
            categories = Category.objects.filter(items__market_name=seller_profile).annotate(num_items=Count('items'))
            auction_items = AuctionItem.objects.filter(user=seller_profile.user, is_sold=False)[:6]
        elif request.user.role == User.CUSTOMER:
            customer_profile = request.user.customerprofile
            items = Item.objects.filter(is_sold=False)[:20]
            auction_items = AuctionItem.objects.filter(user=customer_profile.user, is_sold=False)[:6]
        elif request.user.is_superuser:
            items = Item.objects.all()[:20]
            auction_items = AuctionItem.objects.all()[:10]
            categories = Category.objects.annotate(num_items=Count('items'))
        else:
            items = Item.objects.filter(is_sold=False)[:20]
            auction_items = AuctionItem.objects.filter(is_sold=False)[:10]

    return render(request, 'index.html', {
        'categories': categories,
        'items': items,
        'auction_items': auction_items,

    })

def About(request):
    return render (request, 'About_Us.html')




@csrf_protect
def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect(detect_user_redirect_url(request.user))
    if request.method == 'POST':
        form = UserForm(request.POST)
        c_form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid() and c_form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(form.cleaned_data['password'])
            user.save()
            customer = c_form.save(commit=False)
            customer.user = user
            customer.save()
            messages.success(request, 'Your account has been registered successfully!')
            return redirect('login_view')
    else:
        form = UserForm()
        c_form = CustomerProfileForm()

    return render(request, 'user/signup_costumer.html', {'form': form, 'c_form': c_form})

@csrf_protect
def register_seller(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('signup_seller')
    if request.method == 'POST':
        form = UserForm(request.POST)
        s_form = SellerForm(request.POST, request.FILES)
        if form.is_valid() and s_form.is_valid():
            user = form.save(commit=False)
            user.role = User.SELLER
            user.set_password(form.cleaned_data['password'])
            user.save()
            seller = s_form.save(commit=False)
            seller.user = user
            seller.save()
            messages.success(request, 'Your account has been registered successfully!')
            return redirect('login_view')
    else:
        form = UserForm()
        s_form = SellerForm()
    return render(request, 'user/signup_seller.html', {'form': form, 's_form': s_form})
                                                                                    
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=email, password=password)
        if user is None:  
            messages.error(request, 'User does not exist')
            return render(request, 'user/login_view.html')
        else:
            auth.login(request, user)
            messages.success(request,'YOU are logged in')
            return redirect('index')
    return render(request, 'user/login_view.html')


def logout_view(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('index')

@login_required(login_url='login_view')
def my_account(request):
    return redirect(detect_user_redirect_url(request.user))

@login_required(login_url='login_view')
def CustomerProfiles(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    if request.method == 'POST':
        profile_form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('index')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = CustomerProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)
    
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
    }
    return render(request, 'user/CostumerProfile.html',context)

@login_required(login_url='login_view')
def SellerProfiles(request):
    user = request.user
    profile = get_object_or_404(SellerProfile, user=user)
    if request.method == 'POST':
        profile_form = SellerForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('index')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = SellerForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)
    
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
    }
    return render(request, 'user/SellerProfile.html', context)

@login_required(login_url='login_view')
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login_view')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'user/reset_password.html')

        
@login_required
def seller_dashboard(request):
    user = request.user
    SellerProfile = user.sellerprofile
    items = Item.objects.filter(market_name=SellerProfile)
    item_paginator = Paginator(items, 2)
    item_page_number = request.GET.get('page', 1)
    item_page = item_paginator.get_page(item_page_number)

    auction_items = AuctionItem.objects.filter(user=SellerProfile.user)
    auctions = Auction.objects.filter(item__in=auction_items) if auction_items.exists() else Auction.objects.none()
    auction_paginator = Paginator(auctions, 2)
    auction_page_number = request.GET.get('page', 1)
    auction_page = auction_paginator.get_page(auction_page_number)

    tickets = Ticket.objects.filter(title__in=auctions) if auctions.exists() else Ticket.objects.none()
    ticket_paginator = Paginator(tickets, 2)
    ticket_page_number = request.GET.get('page', 1)
    ticket_page = ticket_paginator.get_page(ticket_page_number)

    # Initialize the sales_data QuerySet
    item_payment = Payment.objects.filter(order__orderitem__item__in=items)
    # item_payment = Payment.objects.filter(order__in=items)
    auction_payment = Payment.objects.filter(auction__in=auctions)
    ticket_payment = Payment.objects.filter(ticket__in=tickets)
    sales_data = Payment.objects.none()
    if item_payment.exists():
        sales_data |= item_payment
    if auction_payment.exists():
        sales_data |= auction_payment
    if ticket_payment.exists():
        sales_data |= ticket_payment
    total_sales = sales_data.aggregate(total=Sum('paid_amount'))['total'] if sales_data.exists() else 0
    context = {
        'items': items,
        'item_page': item_page,
        'auction_items': auction_items,
        'auctions': auctions,
        'auction_page': auction_page,
        'tickets': tickets,
        'ticket_page': ticket_page,
        'sales_data': sales_data,
        'total_sales': total_sales,
        
    }

    return render(request, 'user/dashboard.html', context)

@login_required
def Costumer_dashboard(request):
    users = request.user
    auction_items = AuctionItem.objects.filter(user=users)
    auctions = Auction.objects.filter(item__in=auction_items) if auction_items.exists() else Auction.objects.none()
    auction_paginator = Paginator(auctions, 2)
    auction_page_number = request.GET.get('page', 1)
    auction_page = auction_paginator.get_page(auction_page_number)
    tickets = Ticket.objects.filter(title__in=auctions) if auctions.exists() else Ticket.objects.none()
    ticket_paginator = Paginator(tickets, 2)
    ticket_page_number = request.GET.get('page', 1)
    ticket_page = ticket_paginator.get_page(ticket_page_number)

    sales_data = Payment.objects.none()
    if auctions.exists():
        sales_data = sales_data.union(Payment.objects.filter(auction__in=auctions).distinct())
    if tickets.exists():
        sales_data = sales_data.union(Payment.objects.filter(ticket__in=tickets).distinct())

    total_sales = sales_data.aggregate(total=Sum('paid_amount'))['total'] if sales_data.exists() else 0

    context = {
        'auction_items': auction_items,
        'auctions': auctions,
        'tickets': tickets,
        'auction_page': auction_page,
        'ticket_page': ticket_page,
        'sales_data': sales_data,
        'total_sales': total_sales,
    }
    return render(request, 'user/dashboard.html', context)

@login_required
def super_dashboard(request):
    items = Item.objects.all()
    item_paginator = Paginator(items, 2)
    item_page_number = request.GET.get('page', 1)
    item_page = item_paginator.get_page(item_page_number)

    auction_items = AuctionItem.objects.all()
    auctions = Auction.objects.filter(item__in=auction_items) if auction_items.exists() else Auction.objects.none()
    auction_paginator = Paginator(auctions, 2)
    auction_page_number = request.GET.get('page', 1)
    auction_page = auction_paginator.get_page(auction_page_number)

    tickets = Ticket.objects.all() if auctions.exists() else Ticket.objects.none()
    ticket_paginator = Paginator(tickets, 2)
    ticket_page_number = request.GET.get('page', 1)
    ticket_page = ticket_paginator.get_page(ticket_page_number)

    sales_data = Payment.objects.none()
    if items.exists():
        sales_data = sales_data.union(Payment.objects.filter(order__orderitem__item__in=items).distinct())
    if auctions.exists():
        sales_data = sales_data.union(Payment.objects.filter(auction__in=auctions).distinct())
    if tickets.exists():
        sales_data = sales_data.union(Payment.objects.filter(ticket__in=tickets).distinct())

    total_sales = sales_data.aggregate(total=Sum('paid_amount'))['total'] if sales_data.exists() else 0

    context = {
        'items': items,
        'auction_items': auction_items,
        'auctions': auctions,
        'tickets': tickets,
        'item_page': item_page,
        'auction_page': auction_page,
        'ticket_page': ticket_page,
        'sales_data': sales_data,
        'total_sales': total_sales,
    }

    return render(request, 'user/dashboard.html', context)

