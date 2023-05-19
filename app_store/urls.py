from django.urls import path
from app_store.views import *

urlpatterns = [
    path("", MainPageView.as_view(), name="index"),
    path("product/<str:slug>", ProductView.as_view(), name="product_detail"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("catalog/<int:category_id>", CatalogView.as_view(), name="catalog_category"),
    path("about/", AboutView.as_view(), name="about"),
]
