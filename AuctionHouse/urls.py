"""
URL configuration for food project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import About, index, logout_view, register_user, register_seller, login_view, SellerProfiles, CustomerProfiles, reset_password, seller_dashboard, Costumer_dashboard,super_dashboard 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('admin/', admin.site.urls,name='admin'),
    path('cart/', include('cart.urls')),
    path('items/', include('item.urls')),
    path ('auctions/',include('auctions.urls')),
    # path ('auctions/',include('allauth.urls')),
    path ('ticket/',include('ticket.urls')),
    path ('order/',include('order.urls')),
    path ('payment/',include('payment.urls')),
    path ('chat/',include('chat.urls')),
    path ('',index,name='index'),
    path ('AboutUs',About, name='About_Us'),
    path ('login_view/',login_view,name='login_view'),
    path('register_user/', register_user, name='register_user'),
    path ('signup_seller/',register_seller,name='register_Seller'),
    path('reset_password/',reset_password,name='reset_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout_view/',logout_view, name='logout_view'),
    path('CustomerProfile/',CustomerProfiles,name='CustomerProfile'),
    path('SellerProfile/',SellerProfiles,name='SellerProfile'),
    path('Seller_Dashboard/', seller_dashboard, name='seller_dashboard'),
    path('Costumer_Dashboard/', Costumer_dashboard, name='Costumer_dashboard'),
    path('Dashboard/', super_dashboard, name='super_dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
