from django.urls import path
from images import views as image_views

app_name = "core"

urlpatterns = [
    path("", image_views.HomeView.as_view(), name="home"),
    path("search", image_views.SearchView.as_view(), name="search"),
]
