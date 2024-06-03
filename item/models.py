from django.db import models
from user.models import SellerProfile, User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    class Meta:
        ordering = ('name',)
        verbose_name_plural ='Categories'
    
    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name

class Item(models.Model):
    market_name = models.ForeignKey(SellerProfile, on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(Category, related_name='items',on_delete=models.SET_NULL, default=None, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    image = models.ImageField(null=True,blank=True)
    stock = models.IntegerField(default=1 )
    is_sold = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True, null=True,blank=True)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)], null = True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.item) + " Rating " + str(self.rating)