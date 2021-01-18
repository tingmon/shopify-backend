from django.db import models
from django.urls import reverse
from core import models as core_models
import numpy as np
import pandas as pd
from cv2 import cv2
from colorthief import ColorThief

# Create your models here.
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
# r = g = b = 0
# x = y = 0


class Photo(core_models.TimeStampedModel):
    objects = models.Manager()
    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="photos")
    product = models.ForeignKey(
        "Product", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Product(core_models.TimeStampedModel):
    objects = models.Manager()
    name = models.CharField(max_length=80)
    stock = models.IntegerField(default=0, blank=False)
    price = models.IntegerField(default=0, blank=False)
    in_stock = models.BooleanField(default=False)
    low_stock = models.BooleanField(default=False)
    uploader = models.ForeignKey(
        "users.User", related_name="products", on_delete=models.CASCADE)

    def is_in_stock(self):
        if self.stock > 0:
            self.in_stock = True
        else:
            self.in_stock = False

    def is_low_stock(self):
        if self.in_stock is True:
            if self.stock < 4:
                self.low_stock = True
            else:
                self.low_stock = False
        else:
            self.low_stock = False

    def save(self, *args, **kwargs):
        self.is_in_stock()
        self.is_low_stock()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    def fisrt_photo(self):
        (photo,) = self.photos.all()[:1]
        return photo.file.url

    def get_all_photos(self):
        photos = self.photos.all()[1:]
        print(photos)
        return photos

    # def color_detector(self):
    #     filename = "uploads/" + str(self.file)
    #     color = ColorThief(filename)
    #     dominant_color = color.get_color(10)
    #     print(dominant_color)
    #     r, g, b = dominant_color
    #     b = int(b)
    #     g = int(g)
    #     r = int(r)
    #     self.recognize_color(r, g, b)
    #     pass

    # def recognize_color(self, R, G, B):
    #     minimum = 10000
    #     for i in range(len(csv)):
    #         d = abs(R - int(csv.loc[i, "R"])) + abs(G -
    #                                                 int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
    #         if(d <= minimum):
    #             minimum = d
    #             cname = csv.loc[i, "color_name"]
    #     print(cname)
    #     return cname
