from django import forms
from ticket.models import Ticket ,TicketPurchaseList

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['price','description']

class TicketPurchaseListForm(forms.ModelForm):
    class Meta:
        model = TicketPurchaseList
        fields = ['user']