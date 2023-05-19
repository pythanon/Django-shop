from django.db import models
from singleton_models.models import SingletonModel


class SiteSettings(SingletonModel):
    categories = models.ManyToManyField(
        "app_store.Category",
        related_name="favorite_categories",
        verbose_name="Избранные категории",
    )
    free_delivery_edge = models.PositiveIntegerField(
        default=0, verbose_name="Порог бесплатной доставки"
    )
    cost_usual_delivery = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена обычной доставки"
    )
    cost_express = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена экспресс доставки"
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"
