from django import forms
from django.forms.widgets import TextInput, Textarea, NumberInput, Select
from auctions.models import Auction, Bid, AuctionItem, AuctionPurchase

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    format = '%Y-%m-%dT%H:%M'

class AuctionItemForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = ['item_name', 'description', 'image', 'category']
        widgets = {
            'item_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name', 'aria-label': 'Item Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows': 3, 'placeholder': 'Provide a detailed description', 'aria-label': 'Description'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'aria-label': 'Upload Image'}),
            'category': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Select Category'}),
        }

class AuctionItemUpdateForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = ['item_name', 'description', 'image', 'category']
        widgets = {
            'item_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name', 'aria-label': 'Item Name'}),
            'description': Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows': 3, 'placeholder': 'Provide a detailed description', 'aria-label': 'Description'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'aria-label': 'Upload Image'}),
            'category': Select(attrs={'class': 'form-select', 'aria-label': 'Select Category'}),
        }

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'starting_time', 'end_time', 'start_price']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter auction title', 'aria-label': 'Auction Title'}),
            'starting_time': DateTimeInput(attrs={'class': 'form-control', 'aria-label': 'Starting Time'}),
            'end_time': DateTimeInput(attrs={'class': 'form-control', 'aria-label': 'Ending Time'}),
            'start_price': NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'aria-label': 'Start Price'}),
        }

class UpdateAuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['item', 'starting_time', 'end_time', 'start_price']
        widgets = {
            'item': Select(attrs={'class': 'form-select', 'aria-label': 'Select Item'}),
            'starting_time': DateTimeInput(attrs={'class': 'form-control', 'aria-label': 'Starting Time'}),
            'end_time': DateTimeInput(attrs={'class': 'form-control', 'aria-label': 'Ending Time'}),
            'start_price': NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'aria-label': 'Start Price'}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']
        widgets = {
            'bid_amount': NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'aria-label': 'Bid Amount'}),
        }

class AuctionPurchaseListForm(forms.ModelForm):
    class Meta:
        model = AuctionPurchase
        fields = ['user', 'auction']
        widgets = {
            'user': Select(attrs={'class': 'form-select', 'aria-label': 'Select User'}),
            'auction': Select(attrs={'class': 'form-select', 'aria-label': 'Select Auction'}),
        }
