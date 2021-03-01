from django.urls import path

from . import views

urlpatterns = [
    path("auctions/", views.index, name="index"),
    path("auctions/login", views.login_view, name="login"),
    path("auctions/logout", views.logout_view, name="logout"),
    path("auctions/register", views.register, name="register"),
    path("auctions/new_listing", views.NewListing, name="newlisting"),
    path("auctions/<int:listingid>", views.ListingPage, name="listingpage"),
    path("auctions/category/<int:catid>", views.CategoryListing, name="catlistings"),
    path("auctions/<int:listingid>/", views.AddComment, name="addcomment"),
    path("auctions/<int:listingid>/closed", views.CloseAuction, name="closeauction"),
    path("auctions/add_watchlist/<int:listingid>", views.AddWatchlist, name="addwatchlist"),
    path("auctions/my_watchlist/", views.MyWatchlist, name="watchlist"),
    path("auctions/my_listings/", views.MyListings, name="mylistings"),
    path("auctions/search/", views.Search, name="search")
]
