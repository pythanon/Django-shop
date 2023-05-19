from django.urls import path
from . import views


urlpatterns = [
    path("cart_detail/", views.CartDetail.as_view(), name="cart_detail"),
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
]
