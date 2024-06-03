from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'order'

urlpatterns = [
    path('save_orders/', views.save_orders, name='save_orders'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
