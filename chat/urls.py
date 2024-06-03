from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'chat'

urlpatterns = [

    path('create_room/', views.create_room, name='create_room'),   
    path('chat_room_list/', views.chat_room_list, name='chat_room_list'),
    path('<str:room_name>/', views.chat_room, name='chat_room'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   