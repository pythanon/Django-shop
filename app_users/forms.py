from django import forms

from app_store.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        label="Имя пользователя",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "ivan123"}),
    )
    full_name = forms.CharField(
        max_length=50,
        label="Полное имя",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Иван Иванов"}),
    )
    phone = forms.CharField(
        required=True,
        label="Телефон",
        widget=forms.TextInput(
            attrs={
                "placeholder": "+7-ххх-ххх-хххх",
                "minlength": "12",
                "maxlength": "16",
            }
        ),
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        label="E-mail",
        widget=forms.TextInput(attrs={"placeholder": "example@mail.com"}),
    )
    password1 = forms.CharField(
        max_length=128,
        required=True,
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Введите пароль"}),
    )
    password2 = forms.CharField(
        max_length=128,
        required=True,
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}),
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Такой номер телефона уже зарегистрирован.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой email уже зарегистрирован.")
        return email

    class Meta:
        model = User
        fields = ("username", "full_name", "phone", "email", "password1", "password2")


class MyLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=50,
        required=True,
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
    )
    password = forms.CharField(
        max_length=128,
        label="Пароль",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
    )


class EditProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "Profile-file form-input",
                "type": "file",
                "accept": ".jpg,.gif,.png",
                "data-validate": "onlyImgAvatar",
                "id": "id_avatar",
            }
        ),
    )

    full_name = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "data-validate": "require",
                "placeholder": "Введите ФИО",
                "maxlength": "254",
            }
        ),
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-input", "data-validate": "require"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        label="e-mail",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "data-validate": "require",
                "maxlength": "254",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["avatar", "full_name", "phone", "email"]
