from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import  Category, AuctionListings,Bid,Comments

User= get_user_model()

admin.site.register(User)
admin.site.register(AuctionListings)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comments)


