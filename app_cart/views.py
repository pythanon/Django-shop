from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from app_store.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd["quantity"], update_quantity=cd["update"])
    return redirect("cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")


class CartDetail(TemplateView):
    template_name = "app_cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context["cart"] = cart
        allow_order = True
        for item in cart:
            product = item["product"]
            item["update_quantity_form"] = CartAddProductForm(
                initial={"quantity": item["quantity"], "update": True}
            )
            if product.stock < item["quantity"]:
                allow_order = False
                break
        context["allow_order"] = allow_order
        return context
