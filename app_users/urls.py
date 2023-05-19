from django.urls import path
from app_users.views import *
from django.contrib.auth import views as reset_views

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("register_order/", OrderRegisterView.as_view(), name="register_order"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    path("edit-profile/", EditProfileView.as_view(), name="edit-profile"),
    path("change-password/", MyPasswordChangeView.as_view(), name="change-password"),
    # восстановления пароля
    path(
        "password_reset/",
        reset_views.PasswordResetView.as_view(
            template_name="app_users/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        reset_views.PasswordResetDoneView.as_view(
            template_name="app_users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        reset_views.PasswordResetConfirmView.as_view(
            template_name="app_users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        reset_views.PasswordResetCompleteView.as_view(
            template_name="app_users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
