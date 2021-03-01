from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.forms import ModelForm, Textarea, TextInput
from datetime import datetime
import math
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username.replace("_", " ").title()


class Category(models.Model):
    
    CATEGORY_CHOICES = [
        ('Fashion', 'Fashion'),
        ('Electronics', 'Electronics'),
        ('Toys & Collectibles', 'Toys & Collectibles'),
        ('Books, Movies & Music','Books, Movies & Music')
    ]

    name = models.CharField(max_length=21, choices=CATEGORY_CHOICES)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Condition(models.Model):
    
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Used', 'Used')
    ]

    name = models.CharField(max_length=4, choices=CONDITION_CHOICES)

    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=100)
    image = models.CharField(max_length=200, default="https://raw.githubusercontent.com/SammanthaPS/Images/main/1613805338636.png", blank=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2, default=5.00)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True)
    created_on = models.TimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        widgets = {
            'description': Textarea(attrs={'cols': 50, 'rows': 4}),
        }
        exclude = ['user', 'created_on', 'active']


class Bid(models.Model):
    bid = models.DecimalField(max_digits=8, decimal_places=2, default=1.00)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    created_on = models.TimeField(auto_now_add=True, blank=True)
    
class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid',]


class Comment(models.Model):
    title = models.CharField('title', max_length=30)
    comment = models.CharField(max_length=100)
    created_on = models.DateField(default=datetime.now, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'comment': Textarea(attrs={'cols': 50, 'rows': 4}),
    }
        exclude = ['created_on', 'listing', 'user']


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)





