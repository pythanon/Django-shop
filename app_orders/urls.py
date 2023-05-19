from django.urls import path
from app_orders.views import *

urlpatterns = [
    path("create/", OrderView.as_view(), name="create_order"),
    path("<int:pk>/", OrderDetail.as_view(), name="order_detail"),
    path("pay/<int:pk>/", OrderPayment.as_view(), name="pay"),
    path(
        "pay_progress/<int:order_id>/",
        OrderPaymentProgress.as_view(),
        name="payment_progress",
    ),
    path("history/", HistoryOrders.as_view(), name="history"),
]
