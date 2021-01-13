from django.urls import path
from . import views as image_views

app_name = "images"

urlpatterns = [
    path("<int:pk>", image_views.ProductDetailView.as_view(), name="detail"),
    path("<int:pk>/edit", image_views.ProductEditView.as_view(), name="edit"),
]
