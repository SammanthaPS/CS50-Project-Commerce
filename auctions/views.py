from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import *


def index(request):
    listings = Listing.objects.filter(active=True).order_by('title')
    return render(request, "auctions/index.html", {
        'listings':listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/login.html", {
                "alert": "Error! Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/login.html", {
                "alert": "Error! Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/login.html")


@login_required(login_url='login')
def NewListing(request):
    # will create a new listing.
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            Listing = form.save(commit=False) # create but don't save on database
            Listing.user = request.user # request the current user
            Listing.save() # save to the database

            return render(request, "auctions/newlisting.html", {
                'message':True
            })
        else:
            return render(request, "auctions/newlisting.html")
    else:
        return render(request, 'auctions/newlisting.html')


def ListingPage(request, listingid):
    # will render a page with details of a listing.
    listing = Listing.objects.get(id=listingid)
    comments = Comment.objects.filter(listing=listing)

    def activelisting():
        if listing in Listing.objects.filter(active=True):
            return True
        else:
            return False
    

    def addedwatchlist():
        user = request.user
        added = Watchlist.objects.filter(user=user, listing=listing)
        if added:
            return True
        else:
            return False

    def maxvalue():
        bid = Bid.objects.filter(listing=listing)
        if bid:
            currentbid = float(Bid.objects.filter(listing=listing).aggregate(Max('bid'))['bid__max'])
            maxbid_user = Bid.objects.get(bid=currentbid).user
            return currentbid, maxbid_user
        else:
            return listing.starting_bid, listing.user


    # if empty comments
    def emptycomments():
        if len(comments) == 0:
            return True
        else:
            return False
    

    # returning multiple values from a function.
    a, b = maxvalue()

    # form to place bid
    if request.method == 'POST':
        form = BidForm(request.POST)
        placebid = form.save(commit=False)
        placebid.user = request.user
        placebid.listing = Listing.objects.get(id=listingid)
        
        if a >= placebid.bid:
            return render(request, "auctions/listingpage.html", {
                'alert': True,
                'listing': listing,
                'comments': comments,
                'active': activelisting, 
                'emptycomments': emptycomments,
                'bid': a,
                'maxbiduser': b,
                'added': addedwatchlist,
            })
        else:
            # delete previous bid from the current user.
            #user = request.user
            previousbids = Bid.objects.filter(user=placebid.user, listing=listing)
            previousbids.delete()

            # save new bid
            placebid.save()
            if not Watchlist.objects.filter(user=request.user, listing=listing):
                Watchlist(listing=listing, user=request.user).save() # automatically save to watchlist when place a bid.

            currentbid = float(Bid.objects.filter(listing=listing).aggregate(Max('bid'))['bid__max'])
            maxbid_user = Bid.objects.get(bid=currentbid).user
            return render(request, "auctions/listingpage.html", {
                'success': True,
                'listing': listing,
                'comments': comments,
                'active': activelisting,
                'emptycomments': emptycomments,
                'bid': currentbid,
                'maxbiduser': maxbid_user,
                'added': addedwatchlist,
            })
    else:
        return render(request, "auctions/listingpage.html", {
        'listing': listing,
        'comments': comments,
        'active': activelisting,
        'winner': b,
        'emptycomments': emptycomments,
        'bid': a,
        'maxbiduser': b,
        'added': addedwatchlist,
    })


@login_required(login_url='login')
def AddComment(request, listingid):
    # will create a new comment.
    form = CommentForm(request.POST)
    addcomment = form.save(commit=False)
    addcomment.user = request.user
    addcomment.listing = Listing.objects.get(id=listingid)
    addcomment.save()
    return redirect(reverse("listingpage", args=[listingid]))


def CategoryListing(request, catid):
    categories = Category.objects.get(id=catid)
    listings = Listing.objects.filter(active=True, category=categories).order_by('title')
    return render(request, "auctions/index.html", {
        'listings': listings
    })


def CloseAuction(request, listingid):
    listing = Listing.objects.get(id=listingid)
    listing.active = False
    listing.save()
    return redirect(reverse("listingpage", args=[listingid]))


def AddWatchlist(request, listingid):
    user = request.user
    listing = Listing.objects.get(id=listingid)
    
    if Watchlist.objects.filter(user=user, listing=listing):
        Watchlist.objects.filter(user=user, listing=listing).delete()
        return redirect(reverse("listingpage", args=[listingid]))
    else:
        Watchlist(listing=listing, user=user).save()
        return redirect(reverse("listingpage", args=[listingid]))


def MyWatchlist(request):
    user = request.user
    mywatchlist = Watchlist.objects.filter(user=user)

    def emptywatchlist():
        if len(mywatchlist) == 0:
            return True
        else:
            return False

    return render(request, "auctions/watchlist.html", {
        'listings': mywatchlist,
        'empty': emptywatchlist,
    })


def MyListings(request):
    listings = Listing.objects.filter(user=request.user)

    def emptylisting():
        if len(listings) == 0:
            return True
        else:
            return False


    return render (request, "auctions/mylistings.html", {
        'listings': listings,
        'empty': emptylisting,
    })


def Search(request):
    searchform = request.GET.get("q")
    category = request.GET.get("category")

    if category:
        listings = Listing.objects.filter(Q(category=category, title__icontains=searchform) | Q(category=category, description__icontains=searchform))
    else:
        listings = Listing.objects.filter(Q(title__icontains=searchform) | Q(description__icontains=searchform))
 
    return render(request, "auctions/index.html", {
        'listings': listings,
    })
