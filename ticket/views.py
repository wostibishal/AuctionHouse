from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .form import TicketForm, TicketPurchaseListForm
from auctions.models import Auction
from .models import Ticket
from django import forms
from user.models import User

# Create your views here.
@csrf_protect
def create_ticket(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    ticket = get_object_or_404(Ticket, title=auction)
    if ticket.DoesNotExist():
        if request.user == auction.item.user:
            if request.method == 'POST':
                form = TicketForm(request.POST)
                if form.is_valid():
                    ticket = form.save(commit=False)
                    ticket.title = auction  # Set the auction as the title for the ticket
                    ticket.save()
                    messages.success(request, 'Ticket created successfully')
                    return redirect('index')
                else:
                    messages.error(request, 'There was something wrong with the form')
            else:
                form = TicketForm()
        else:
            messages.error(request, 'You are not authorized to create this ticket')
            return redirect('index')
    else:
        messages.info(request,'ticket has been created before')
        return redirect ('list_ticket')
    return render(request, 'ticket/create_ticket.html', {'form': form, 'auction': auction})

def list_ticket(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket/ticket_list.html', {'tickets': tickets})


def purchase_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        form = TicketPurchaseListForm(request.POST)
        if form.is_valid():
            ticket_purchase = form.save(commit=False)
            ticket_purchase.user = request.user  # Automatically set the logged-in user
            ticket_purchase.ticket = ticket
            ticket_purchase.save()
            return redirect('index')
        else:
            messages.error(request, 'There was something wrong with the form')
    else:
        form = TicketPurchaseListForm(initial={'user': request.user })
        form.fields['user'].widget = forms.HiddenInput()
    return render(request, 'ticket/purchase_ticket.html', {'form': form, 'ticket': ticket})

def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.user == ticket.title.item.user:
        if request.method == 'POST':
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ticket updated successfully')
                return redirect('index')
            else:
                messages.error(request, 'There was something wrong with the form')
        else:
            form = TicketForm(instance=ticket)
    else:
        messages.error(request, 'You are not authorized to edit this ticket')
        return redirect('index')
    return render(request, 'ticket/ticket_update.html', {'form': form, 'ticket': ticket})

def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    user = request.user
    if user:    
        if request.method == 'POST':
                ticket.delete()
                messages.success(request, 'ticket deleted') 
        else:
            messages.error(request, 'something went wrong.')
    elif request.user.is_superuser:
        if request.method == 'POST': 
                ticket.delete()
                messages.success(request, 'ticket deleted') 
        else:
            messages.error(request, 'something went wrong.')
    return redirect('index')