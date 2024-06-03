from django.urls import path
from . import views


app_name = 'ticket'

urlpatterns = [
    path ('<int:pk>/create_ticket/', views.create_ticket,name='create_ticket'),
    path('purchase_ticket/<int:ticket_id>/', views.purchase_ticket, name='purchase_ticket'),
    path ('ticket/list_ticket/', views.list_ticket, name='list_ticket'),
    path ('ticket_update/<int:ticket_id>/', views.ticket_update, name='ticket_update'),
    path ('ticket_delete/<int:ticket_id>/', views.ticket_delete, name='ticket_delete'),
]