# Commerce - CS50'S Web Programming with Python and JavaScript - Commerce

Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add to a "watchlist".

# Specification

* Models: Your application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.

* Create Listing: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.

* Active Listings Page: The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).

* Listing Page: Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
  * If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it.
  * If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other   bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
  * If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
  * If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
  * Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.

* Watchlist: Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.

* Categories: Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.

* Django Admin Interface: Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.

# General Usage Notes

In the distribution code is a Django project called `commerce` that contains a single app called `auctions`.

Take a look at `auctions\models.py` to see the models for User, Category, Condition, Listing, Bid, Comment and Watchlist.

On `auctions\views.py` there are 12 functions to fulfill the specification listed above.
  1. `User` for authentication.
  2. `index` the default route of my web aplication.
      * On the index page, the user will be able to select a category, sign in/register, or search for a listing.
  2. `login`, `logout` and `register` for authentication purpose.
  3. `NewListing` to create a new listing.
  4. `ListingPage` will render a page with details of a listing.
      * If the current user is different from the seller, the user will be able to bid, add to watchlist and make a comment.
      * If the user choose to place bid, the listing will be automatically saved on Watchlist.
  5. `AddComment` to create a new comment on the listing.
  6. `CategoryListing` to render a page for the selected category.
  7. `CloseAuction` to close the auction and announce the highest bidder the winner.
  8. `AddWatchlist` to add a listing to watchlist in case the user doesn't bid.
  9. `MyWatchlist` will render a page with all the listings saved on watchlist.
  10. `MyListings` will render a page with all listings made by current user.
  11. `Search` to lookup for a specific listing.

On `static\auctions` there are 2 folders. One for the `CSS` and another one for the `Images` used in this project.

Finally, take a look at `templates\auctions` to see all the templates associated with `auctions\views.py`.

If you want to see a demonstration of my project functionality: **<https://youtu.be/ru10OMHEbp8>**

