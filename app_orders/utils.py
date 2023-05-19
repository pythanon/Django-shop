from app_settings.models import SiteSettings


def get_delivery_price(total, type_delivery):
    settings = SiteSettings.objects.first()
    usual_delivery_price = settings.cost_usual_delivery
    edge_delivery = settings.free_delivery_edge
    express_delivery_price = settings.cost_express
    if type_delivery == "2":
        return express_delivery_price
    if total < edge_delivery:
        return usual_delivery_price
    else:
        return 0
