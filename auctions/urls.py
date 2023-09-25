from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create"),
    path("category", views.categories, name="categories"),
    path("category/<str:title>",views.category, name="category"),
    path("listing/<int:id>",views.listing, name="listing"),
    path("listing/<int:id>/comment",views.comment, name="comment"),
    path("addwatchlist/<int:id>",views.addwatchlist, name="addwatch"),
    path("remwatchlist/<int:id>",views.remove_watchlist, name="remove"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("listing/<int:id>/bid",views.bid, name="bid"),
    path("addwatchlist/<int:id>/end",views.endAuction, name="end")
]
