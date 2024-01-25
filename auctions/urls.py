from django.urls import path

from . import views

urlpatterns = [
    path("", views.AuctionListing.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.AuctionFormView.as_view(), name="create"),
    path("category", views.CategoryList.as_view(), name="categories"),
    path("category/<str:title>", views.CategoryDetail.as_view(), name="category"),
    path("listing/<int:pk>",views.AuctionDetail.as_view(), name="listing"),
    path("listing/<int:pk>/comment",views.Comment.as_view(), name="comment"),
    path("watchlist/<int:pk>",views.WatchListDetail.as_view(), name="watch"),
    path("watchlist",views.WatchListList.as_view(), name="watchlist"),
    path("listing/<int:pk>/bid",views.BidView.as_view(), name="bid"),
]
