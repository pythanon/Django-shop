from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView
from django_filters.views import FilterView

from app_cart.forms import CartAddProductForm, CartAddProductDetailForm
from app_store.filters import ProductFilter
from app_store.forms import ReviewForm
from app_store.models import *
from app_settings.models import SiteSettings
from app_store.utils import get_range_price


class MainPageView(View):
    def get(self, request):
        site_settings = SiteSettings.objects.first()
        banners = Product.objects.annotate(num_reviews=Count("reviews")).order_by(
            "-num_reviews"
        )[:3]
        favorite_categories = site_settings.categories.all()[:3]
        popular_products = Product.objects.filter(available=True).order_by(
            "-sort_index", "-purchases_num"
        )[:8]
        limited_products = Product.objects.filter(available=True, limited=True)
        cart_product_form = CartAddProductForm()
        return render(
            request,
            "app_store/index.html",
            {
                "popular_products": popular_products,
                "limited_products": limited_products,
                "banners": banners,
                "favorite_categories": favorite_categories,
                "cart_product_form": cart_product_form,
            },
        )


class ProductView(DetailView):
    model = Product
    template_name = "app_store/product.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Reviews.objects.filter(product=self.object)
        context["form"] = CartAddProductDetailForm()
        context["form"].fields["quantity"].widget.attrs["max"] = self.object.stock
        context["review_form"] = ReviewForm
        return context

    def post(self, request, slug):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user.profile
            review.product = self.get_object()
            review.save()
        return redirect("product_detail", slug=slug)


class CatalogView(FilterView):
    template_name = "app_store/catalog.html"
    model = Product
    context_object_name = "products_list"
    filterset_class = ProductFilter
    paginate_by = 8
    category = None

    def get_queryset(self):
        queryset = super(CatalogView, self).get_queryset()
        queryset = queryset.filter(available=True)

        category_id = self.kwargs.get("category_id", 0)
        if category_id:
            self.category = Category.objects.filter(pk=category_id)
            if self.category.exists():
                self.category = self.category.first()
                queryset = queryset.filter(
                    Q(category=self.category) | Q(category__parent=self.category)
                )
        return queryset

    def get_context_data(self, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop("page", True) and _request_copy.urlencode()
        cart_product_form = CartAddProductForm()

        context = super().get_context_data(**kwargs)

        context["parameters"] = parameters
        context["cart_product_form"] = cart_product_form
        price_range = get_range_price(self.category)

        context["filter"].form.fields["price"].widget.attrs = {
            "class": "range-line",
            "data-type": "double",
            "data-min": price_range["min_price"],
            "data-max": price_range["max_price"],
        }

        return context


class AboutView(TemplateView):
    template_name = "app_store/about.html"
