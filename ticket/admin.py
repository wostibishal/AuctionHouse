from django.contrib import admin
from ticket.models import Ticket, TicketPurchaseList

# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title','price', 'description')

admin.site.register(Ticket , TicketAdmin )
admin.site.register(TicketPurchaseList )