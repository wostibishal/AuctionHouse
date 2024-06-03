from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.item_detail, name='item_detail'),
    path ('add_product/', views.item_add, name='item_add'),
    path('<int:pk>/update/',views.item_update, name='item_update'),
    path('<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('item_list/', views.item_list, name='item_list'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)