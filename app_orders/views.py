import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormMixin, UpdateView

from app_cart.cart import Cart
from app_orders.forms import OrderCreateForm, OrderPaymentForm
from app_orders.models import OrderItem, Order
from app_orders.utils import get_delivery_price
from app_settings.models import SiteSettings
from app_store.models import Product
from app_users.forms import RegisterForm


class OrderView(FormMixin, TemplateView):
    template_name = "app_orders/order.html"
    form_class = OrderCreateForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        total_cost = cart.get_total_price()
        choices = []
        settings = SiteSettings.objects.first()
        usual_delivery_price = settings.cost_usual_delivery
        edge_delivery = settings.free_delivery_edge
        express_delivery_price = settings.cost_express

        if total_cost < edge_delivery:
            choices.append(("1", f"Обычная доставка (+{usual_delivery_price} руб.)"))
            context["price_usual"] = usual_delivery_price
        else:
            choices.append(("1", f"Обычная доставка (бесплатно)"))
            context["price_usual"] = 0

        context["total_with_delivery"] = total_cost + get_delivery_price(
            total=cart.get_total_price(), type_delivery="1"
        )
        choices.append(("2", f"Экспресс доставка (+{express_delivery_price} руб.)"))
        context["form"].fields["delivery_type"].widget.choices = choices
        if self.request.user.is_authenticated:
            instance = self.request.user.profile
            context["form_reg"] = RegisterForm(instance=instance)
            context["form_reg"].fields["username"].disabled = True
            context["form_reg"].fields["full_name"].disabled = True
            context["form_reg"].fields["phone"].disabled = True
            context["form_reg"].fields["email"].disabled = True
        else:
            context["form_reg"] = RegisterForm()
        return context

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.data = form.cleaned_data
            order.profile = request.user.profile
            order.delivery_price = get_delivery_price(
                total=cart.get_total_price(),
                type_delivery=form.cleaned_data["delivery_type"],
            )
            order.city = form.cleaned_data["city"]
            objs = list()
            for item in cart:
                objs.append(
                    OrderItem(
                        order=order,
                        product=item["product"],
                        price=item["price"],
                        quantity=item["quantity"],
                    )
                )
            order.save()
            OrderItem.objects.bulk_create(objs)

            objs_store = list()
            for good in order.items.all():
                store_good = Product.objects.select_for_update().get(id=good.product.id)
                store_good.stock -= good.quantity
                store_good.purchases_num += 1
                objs_store.append(store_good)
            Product.objects.bulk_update(objs_store, ["stock", "purchases_num"])

            cart.clear()
            return HttpResponseRedirect(reverse("pay", args=[order.id]))
        return super().form_invalid(form)


class OrderPayment(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderPaymentForm
    template_name = "app_orders/payment.html"
    raise_exception = True

    def get_object(self, queryset=None):
        order = super().get_object(queryset)
        if order.profile != self.request.user.profile:
            raise PermissionDenied
        return order

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        form = OrderPaymentForm(request.POST, instance=order)

        if form.is_valid():
            card_number = form.cleaned_data["card_number"]
            errors_list = [
                "Счет заблокирован",
                "Неправильный номер счета",
                "Ошибка сервера",
                "Недостаточно средств",
                "Банк отклонил платеж",
            ]

            order = form.save(commit=False)

            if int(card_number) % 2 or card_number[-1] == "0":
                status = random.choice(errors_list)
                payment_code = 2
            else:
                status = "Оплачен"
                payment_code = 1
                order.paid = True

            order.status = status
            order.payment_code = payment_code
            order.save()
            return HttpResponseRedirect(
                reverse("payment_progress", kwargs={"order_id": order.id})
            )
        return super().form_invalid(form)


class OrderPaymentProgress(LoginRequiredMixin, TemplateView):
    template_name = "app_orders/progressPayment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs["order_id"]
        print(order_id)
        context["order_id"] = order_id
        return context


class OrderDetail(LoginRequiredMixin, DetailView):
    template_name = "app_orders/oneorder.html"
    raise_exception = True
    model = Order
    context_object_name = "order"

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.profile != self.request.user.profile:
            raise PermissionDenied
        return object


class HistoryOrders(LoginRequiredMixin, ListView):
    template_name = "app_orders/historyorder.html"
    raise_exception = True
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        queryset = Order.objects.only(
            "id", "created", "paid", "delivery_type", "payment_type", "paid", "status"
        ).filter(profile=self.request.user.profile)
        return queryset
