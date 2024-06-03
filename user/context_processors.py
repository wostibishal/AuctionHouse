from .models import CustomerProfile, SellerProfile
from django.conf import settings

def get_Seller(request):
    try:
        seller = SellerProfile.objects.get(user=request.user)
    except:
        seller = None
    return dict(seller=seller)


def get_Costumer(request):
    try:
        Costumer= CustomerProfile.objects.get(user=request.user)
    except:
        Costumer = None
    return dict(Costumer=Costumer)

