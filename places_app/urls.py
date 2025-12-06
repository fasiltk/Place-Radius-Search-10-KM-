from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_place, name="add_place"),
    path("search/", views.search_nearby, name="search_nearby"),
]
