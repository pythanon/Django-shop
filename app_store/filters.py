import django_filters
from django import forms

from django_property_filter import PropertyBooleanFilter
from django_property_filter import PropertyFilterSet
from django_property_filter import PropertyOrderingFilter

from .utils import *
from .widgets import ShopCheckboxInput
from .widgets import ShopLinkWidget


class ProductFilter(PropertyFilterSet):
    title = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={"class": "form-input form-input_full", "placeholder": "Название"}
        ),
    )
    is_stock = PropertyBooleanFilter(field_name="is_stock", widget=ShopCheckboxInput)
    is_limited = PropertyBooleanFilter(field_name="limited", widget=ShopCheckboxInput)

    price = django_filters.CharFilter(
        method="price_range",
        field_name="price",
        lookup_expr="range",
        widget=forms.TextInput(
            attrs={
                "class": "range-line",
                "data-type": "double",
                "data-min": get_range_price()["min_price"],
                "data-max": get_range_price()["min_price"],
            }
        ),
    )

    order_by_field = "ordering"
    ordering = PropertyOrderingFilter(
        choices=(
            ("price", "Цене"),
            ("-price", "Цене"),
            ("created", "Новизне"),
            ("-created", "Новизне"),
            ("purchases_num", "Популярности"),
            ("-purchases_num", "Популярности"),
            ("reviews_count", "Отзывам"),
            ("-reviews_count", "Отзывам"),
        ),
        fields=["price", "created", "purchases_num", "reviews_count"],
        empty_label=None,
        widget=ShopLinkWidget,
    )

    @staticmethod
    def price_range(queryset, _, value):
        return queryset.filter(price__range=value.split(";"))

    class Meta:
        model = Product
        order_by_field = "price"
        fields = ("price", "title", "is_stock", "is_limited")
