from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cart'

urlpatterns = [

    path('view/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   