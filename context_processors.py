from app_cart.cart import Cart
from app_settings.models import SiteSettings
from app_store.models import Category

def site_context(request):
    site_settings = SiteSettings.objects.first()
    categories = Category.objects.filter(parent=None)

    return {'site_settings': site_settings,
            'categories': categories,
            'cart': Cart(request)}
