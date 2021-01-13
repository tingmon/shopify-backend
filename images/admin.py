from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Product)
class CustomProductAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)
    list_display = (
        "name",
        "uploader",
        "stock",
        "price",
        "in_stock",
    )


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = (
        "__str__",
        "get_thumnail",
    )

    def get_thumnail(self, obj):
        print(obj.file.url)
        return mark_safe(f'<img width="50px" src="{obj.file.url}"/>')

    get_thumnail.short_description = "Thumnail"
