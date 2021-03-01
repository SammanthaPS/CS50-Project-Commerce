from django.contrib import admin

from .models import *
# Register your models here.


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'active', 'starting_bid', 'description')
    list_filter = ('user',)

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('bid', 'user', 'listing')
    list_filter = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'comment', 'listing', 'user')

