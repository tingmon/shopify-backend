from django.urls import path
from . import views as image_views

app_name = "images"

urlpatterns = [
    path("<int:pk>", image_views.ProductDetailView.as_view(), name="detail"),
    path("<int:pk>/edit", image_views.ProductEditView.as_view(), name="edit"),
    path("<int:pk>/photos", image_views.ProductPhotoView.as_view(), name="photos"),
    path(
        "<int:product_pk>/photos/<int:photo_pk>/delete",
        image_views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:product_pk>/photos/<int:photo_pk>/edit",
        image_views.PhotoEditView.as_view(),
        name="edit-photo",
    ),
]
