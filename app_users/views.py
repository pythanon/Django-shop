from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import PasswordInput
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from app_orders.models import Order
from app_users.forms import RegisterForm, MyLoginForm, EditProfileForm
from app_users.models import Profile


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "app_users/register.html"
    success_url = reverse_lazy("profile")
    login_url = reverse_lazy("login")

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse("profile"))
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")

        Profile.objects.create(
            user=self.object,
            username=username,
            full_name=form.cleaned_data["full_name"],
            phone=form.cleaned_data["phone"],
            email=form.cleaned_data["email"],
        )

        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class OrderRegisterView(RegisterView):
    success_url = reverse_lazy("create_order")


class MyLogoutView(LogoutView):
    next_page = "/"


class MyLoginView(LoginView):
    template_name = "app_users/login.html"
    authentication_form = MyLoginForm

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse("profile"))
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        else:
            return reverse("profile")


@login_required
def profile(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    last_order = Order.objects.filter(profile=user_profile).first()
    context = {
        "avatar": user_profile.avatar.url if user_profile.avatar else None,
        "full_name": user_profile.full_name,
        "last_order": last_order,
    }
    return render(request, "app_users/profile.html", context)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "app_users/edit-profile.html"
    success_url = reverse_lazy("edit-profile")
    form_class = EditProfileForm

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно сохранен")
        return super(EditProfileView, self).form_valid(form)


class MyPasswordChangeView(PasswordChangeView):
    template_name = "app_users/change-password.html"
    success_url = reverse_lazy("change-password")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget = PasswordInput(
            attrs={"class": "form-input", "placeholder": "Введите текущий пароль"}
        )
        form.fields["new_password1"].widget = PasswordInput(
            attrs={"class": "form-input", "placeholder": "Введите новый пароль"}
        )
        form.fields["new_password2"].widget = PasswordInput(
            attrs={"class": "form-input", "placeholder": "Повторите новый пароль"}
        )
        return form

    def form_valid(self, form):
        messages.success(self.request, "Пароль успешно обновлен.")
        return super().form_valid(form)
