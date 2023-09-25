from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateAuctionForm, CommentFieldForm
from .models import User, AuctionListings,Category, Comments,Bid

def index(request):
    listing = AuctionListings.objects.filter(is_active=True).all()
    if request.user.is_authenticated:
        expired = AuctionListings.objects.filter(is_active=False, bidwinner=request.user)
        bought = False
        if expired.count() > 0:
            bought = True
        return render(request, "auctions/index.html", {
            'items' : listing,
            'buys' : expired,
            'bought' : bought
        })
    return render(request, "auctions/index.html", {
            'items' : listing
        })


@login_required
def create_listing(request):
    form = CreateAuctionForm()
    if request.method == 'GET':
        return render(request, "auctions/create.html",{
            "form": form
        })
    if request.method == 'POST':
        form = CreateAuctionForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "message": 'unsuccessful submission',
                "form": form
            })

    
def listing(request,id):
    listing = AuctionListings.objects.get(pk=id)
    watch = request.user in listing.watchlist.all()
    form = CommentFieldForm()
    comment = Comments.objects.filter(listing=listing)
    return render(request, "auctions/listing.html", {
        'item' : listing,
        'watch' : watch,
        'comments' : comment,
        'form' : form
    })


def categories(request):
    all_category = Category.objects.all()
    listings = AuctionListings.objects.filter()
    return render(request, "auctions/categories.html", {
    'items' : listings,
    'category' : all_category
})

def category(request, title):
    category= Category.objects.get(title=title)
    listings = AuctionListings.objects.filter(category=category, is_active= True)
    return render(request, "auctions/index.html", {
        'items' : listings
    })


@login_required
def comment(request, id):   
    listing = AuctionListings.objects.get(pk=id)
    if request.method == 'POST':
        form = CommentFieldForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.listing = listing
            form.save()
            return HttpResponseRedirect(reverse("listing",args=(id, )))


def watchlist(request):
    if request.user.is_authenticated:
        listing = request.user.watchlist.all()
    return render(request, "auctions/index.html", {
        'items' : listing
    })


@login_required
def addwatchlist(request, id):
    listing = AuctionListings.objects.get(pk=id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing",args=(id, )))


@login_required
def remove_watchlist(request, id):
    listing = AuctionListings.objects.get(pk=id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing",args=(id, )))


@login_required
def bid(request, id):
    listing=AuctionListings.objects.get(pk=id)
    bidValue=float(request.POST['bid'])
    (bid, created) = Bid.objects.get_or_create(listing=listing, user=request.user, placed_bid=bidValue)
    if bidValue > listing.price and request.user != listing.user:
        bid.user=request.user
        bid.placed_bid=bidValue
        bid.save()
        listing.price = bidValue
        listing.bidwinner = request.user
        listing.save()
    return HttpResponseRedirect(reverse('listing', args=(id, )))


@login_required
def endAuction(request, id):
    listing=AuctionListings.objects.get(pk=id)
    if request.user.is_authenticated and listing.user == request.user:
        listing.is_active = False
        listing.watchlist.clear()
        listing.save()
    return HttpResponseRedirect(reverse('listing', args=(id, )))


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
