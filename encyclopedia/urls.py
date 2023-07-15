from django.urls import path

from . import views
app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("/create_page", views.create_page, name="create_page"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit_page"),
    path("random", views.random_page, name="random_page"),
]
