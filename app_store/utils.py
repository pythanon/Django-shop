from django.db.models import Q
from app_store.models import Category, Product


def get_range_price(category: Category = None):
    min_price = 0
    max_price = 0
    if category is None:
        product = Product.objects.filter(available=True)
    else:
        product = Product.objects.filter(
            Q(category=category) | Q(category__parent=category), available=True
        )

    product_min_price = product.order_by("price").values("price")
    product_max_price = product.order_by("-price").values("price")

    if product_min_price.exists():
        product_min_price: dict = product_min_price.first()
        min_price = product_min_price.get("price", 0)

    if product_max_price.exists():
        product_max_price: dict = product_max_price.first()
        max_price = product_max_price.get("price", 0)

    return {"min_price": min_price, "max_price": max_price}
