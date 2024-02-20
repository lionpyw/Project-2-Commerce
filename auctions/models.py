from django.db import models
from django.conf import settings

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class AuctionListings(models.Model):
    title = models.CharField(max_length=32)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name='category')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    is_active = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='watchlist',blank=True)
    bidwinner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title


class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='owner')
    listing = models.ForeignKey(AuctionListings, on_delete=models.PROTECT, related_name='listing')
    placed_bid = models.DecimalField(max_digits=6,decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.user} bid on {self.listing}'

class Comments(models.Model):
    listing = models.ForeignKey(
        AuctionListings, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='commentry')
    text = models.TextField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['date']

    def __str__(self):
        return f'{self.user} commented on {self.listing}'