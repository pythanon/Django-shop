from django.contrib.auth.models import User
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Profile(models.Model):
    def validate_image(fieldfile_obj):
        file_size = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if file_size > megabyte_limit * 1024 * 1024:
            raise ValidationError(
                "Максимальный размер файла {}MB".format(str(megabyte_limit))
            )

    user = models.OneToOneField(
        User, unique=True, on_delete=models.CASCADE, related_name="profile"
    )
    username = models.CharField(unique=True, max_length=50, verbose_name="username")
    full_name = models.CharField(max_length=50, verbose_name="ФИО пользователя")
    phoneRegex = RegexValidator(regex=r"^\+7[\-\s]?\d{3}[\-\s]?\d{3}[\-\s]?\d{4}$")
    phone = models.CharField(
        max_length=16,
        verbose_name="номер телефона",
        unique=True,
        validators=[phoneRegex],
    )
    email = models.EmailField(verbose_name="email пользователя", unique=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        validators=[
            validate_image,
            FileExtensionValidator(allowed_extensions=["png", "jpg", "gif"]),
        ],
        default="",
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return self.full_name
