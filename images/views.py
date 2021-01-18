from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, View, UpdateView
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib import messages
from . import models, forms

# Create your views here.

global_qs = ""


class HomeView(ListView):
    model = models.Product
    paginate_by = 5
    paginate_orphans = 1
    page_kwarg = "page"
    ordering = "created"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = models.Product


class SearchView(View):
    def get(self, request):
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            min_price = form.cleaned_data.get("min_price")
            max_price = form.cleaned_data.get("max_price")
            in_stock = form.cleaned_data.get("in_stock")

            # if request.session['name'] == "":
            #     request.session['name'] = name
            # if request.session['min_price'] == "":
            #     request.session['min_price'] = min_price
            # if request.session['max_price'] == "":
            #     request.session['max_price'] = max_price
            # if request.session['in_stock'] == "":
            #     request.session['in_stock'] = in_stock
            # print(max_price)
            # print(request.session['max_price'])

            filter_args = {}
            if str(name).strip() != "":
                filter_args["name__contains"] = name
            if max_price is not None:
                filter_args["price__lte"] = max_price
            if min_price is not None:
                filter_args["price__gte"] = min_price
            if in_stock is True:
                filter_args["in_stock"] = True

            if(len(filter_args) == 0):
                qs = models.Product.objects.all().order_by("created")
            else:
                qs = models.Product.objects.filter(
                    **filter_args).order_by("created")

            num = int(request.GET.get("page", 0))
            print(filter_args)
            print(qs)
            print(num)
            # print(request.session['qs'])

            paginator = Paginator(qs, 5, 1)
            page = request.GET.get("page", 1)
            products = paginator.get_page(page)
            # print(images.has_next())
            # print(images.has_previous())
            # print(dir(products))
            # print(form)

            return render(
                request, "search.html", {"form": form, "products": products}
            )
        else:
            form = forms.SearchForm()
            return render(
                request, "search.html", {"form": form}
            )


class ProductEditView(UpdateView):
    model = models.Product
    template_name = "images/product_edit.html"
    fields = (
        "name",
        "stock",
        "price",
    )

    def get_object(self, queryset=None):
        product = super().get_object(queryset=queryset)
        print(queryset)
        if product.uploader.pk != self.request.user.pk:
            raise Http404("you are not the uploader of this product")
        print(product.uploader.pk, self.request.user.pk)
        print(product)
        return product


class ProductPhotoView(ProductDetailView):

    model = models.Product
    template_name = "images/photo_list.html"

    def get_object(self, queryset=None):
        product = super().get_object(queryset=queryset)
        if product.uploader.pk != self.request.user.pk:
            raise Http404("Unauthorized action requested")
        return product


def delete_photo(request, product_pk, photo_pk):
    user = request.user
    print(dir(request))
    try:
        product = models.Product.objects.get(pk=product_pk)
        if product.uploader.pk is not user.pk:
            messages.error(request, "Unauthorized access")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo deleted")
        return redirect(reverse("images:photos", kwargs={"pk": product_pk}))
    except models.Product.DoesNotExist:
        return redirect(reverse("core:home"))


class PhotoEditView(UpdateView):
    model = models.Photo
    template_name = "images/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    fields = (
        "caption",
        "file",
    )

    def get_success_url(self):
        product_pk = self.kwargs.get("product_pk")
        messages.success(self.request, "Photo Edited")
        return reverse("images:photos", kwargs={"pk": product_pk})


# def preserve_query(qs, num):
#     if num == 0:
#         global_qs = qs
#         print("y")
#         print(global_qs)
#         return global_qs
#     else:
#         print("n")
#         return global_qs

    # def search(request):
    #     name = request.GET.get("name", "")
    #     min_price = int(request.GET.get("min_price", 0))
    #     max_price = int(request.GET.get("max_price", 0))
    #     in_stock = bool(request.GET.get("in_stock", False))

    #     request.session['name'] = name
    #     request.session['min_price'] = min_price
    #     request.session['max_price'] = max_price
    #     request.session['in_stock'] = in_stock

    #     print(request.session['name'])

    #     form = {
    #         "name": request.session['name'],
    #         "min_price": request.session['min_price'],
    #         "max_price": request.session['max_price'],
    #         "in_stock": request.session['in_stock'],
    #     }

    #     filter_args = {}
    #     if str(name).strip() != "":
    #         filter_args["name__contains"] = name
    #     if max_price is not None:
    #         filter_args["price__lte"] = max_price
    #     if min_price is not None:
    #         filter_args["price__gte"] = min_price
    #     if in_stock is True:
    #         filter_args["in_stock"] = True

    #     print(filter_args)

    #     if(len(filter_args) == 2):
    #         qs = models.Product.objects.all()
    #     else:
    #         qs = models.Product.objects.filter(
    #             **filter_args).order_by("created")
    #     print(qs)

    #     paginator = Paginator(qs, 2, 1)
    #     page = request.GET.get("page", 1)
    #     products = paginator.get_page(page)

    #     return render(
    #         request,
    #         "test_search.html",
    #         {**form, "products": products}
    #     )

    # def all_photos(request):
    #     return render(
    #         request,
    #         "search.html"
    #     )
