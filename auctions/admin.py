from django.contrib import admin
from .models import  Category, AuctionListings,Bid,Comments


admin.site.site_header = "Auction Store Admin"
admin.site.index_title = "Admin"

@admin.register(AuctionListings)
class AuctionListingsAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "category", "is_active"]
    prepopulated_fields = {
        'slug': ['title']
    }
    search_fields = ['title']
    list_filter = ["category", "is_active"]


admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comments)


