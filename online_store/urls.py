from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("app_store.urls")),
        path("", include("app_users.urls")),
        path("cart/", include("app_cart.urls")),
        path("orders/", include("app_orders.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
