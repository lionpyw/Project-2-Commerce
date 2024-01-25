from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import CreateAuctionForm, CommentFieldForm
from .models import AuctionListings,Category, Comments,Bid

User = get_user_model()

class AuctionListing(APIView):

    def get(self, request):
        listing = AuctionListings.objects.filter(is_active=True).all()
        if self.request.user.is_authenticated:
            expired = AuctionListings.objects.filter(is_active=False, bidwinner= self.request.user)
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

    @permission_classes([permissions.IsAuthenticated])
    def post(self,request):
        form = CreateAuctionForm(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "message": 'unsuccessful submission',
                "form": form
            })

class AuctionFormView(FormView):
    template_name = "auctions/create.html"
    form_class = CreateAuctionForm
    success_url = "/index/"  
            
class AuctionDetail(APIView):
    def get(self,request,pk):
        listing = AuctionListings.objects.get(pk=pk)
        watch = self.request.user in listing.watchlist.all()
        form = CommentFieldForm()
        comment = Comments.objects.filter(listing=listing)
        return render(request, "auctions/listing.html", {
            'item' : listing,
            'watch' : watch,
            'comments' : comment,
            'form' : form
        })
    
    @permission_classes([permissions.IsAuthenticated])
    def post(self, request, pk):
        listing=AuctionListings.objects.get(pk=pk)
        if listing.user == request.user:
            listing.is_active = False
            listing.watchlist.clear()
            listing.save()
        return HttpResponseRedirect(reverse('listing', args=(pk, )))
    
class CategoryList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'auctions/categories.html'

    def get(self, request):
        all_category = Category.objects.all()
        listings = AuctionListings.objects.filter()
        return Response({
        'items' : listings,
        'category' : all_category
    })

class CategoryDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "auctions/index.html"
    def get(self,request, title):
        category= Category.objects.get(title=title)
        listings = AuctionListings.objects.filter(category=category, is_active= True)
        return Response({
            'items' : listings
        })
    
class WatchListList(APIView):
    def get(self,request):
        if self.request.user.is_authenticated:
            listing = self.request.user.watchlist.all()
        return render(request, "auctions/index.html", {
            'items' : listing
        })

class WatchListDetail(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,pk):
        listing = AuctionListings.objects.get(pk=pk)
        listing.watchlist.add(self.request.user)
        return HttpResponseRedirect(reverse("listing", args=(pk,)))
    
    def post(self, request, pk):
        listing = AuctionListings.objects.get(pk=pk)
        listing.watchlist.remove(self.request.user)
        return HttpResponseRedirect(reverse("listing",args=(pk,)))


class Comment(APIView):   
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request, pk):   
        listing = AuctionListings.objects.get(pk=pk)
        if request.method == 'POST':
            form = CommentFieldForm(request.POST)
            if form.is_valid():
                form.instance.user = self.request.user
                form.instance.listing = listing
                form.save()
                return HttpResponseRedirect(reverse("listing",args=(pk, )))
            
class BidView(APIView):
    @permission_classes([permissions.IsAuthenticated])
    def post(self, request, pk):
        listing=AuctionListings.objects.get(pk=pk)
        bidValue=float(self.request.POST['bid'])
        (bid, _) = Bid.objects.get_or_create(listing=listing, user=self.request.user, placed_bid=bidValue)
        if bidValue > listing.price and self.request.user != listing.user:
            bid.user = self.request.user
            bid.placed_bid = bidValue
            bid.save()
            listing.price = bidValue
            listing.bidwinner = self.request.user
            listing.save()
        return HttpResponseRedirect(reverse('listing', args=(pk, )))


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
