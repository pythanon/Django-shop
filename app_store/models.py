from autoslug import AutoSlugField
from django.db import models
from django.db.models import Min, Q
from django.urls import reverse
from app_settings.models import SiteSettings
from app_users.models import Profile


class Product(models.Model):
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="category",
        verbose_name="Категория",
    )
    name = models.TextField(max_length=50, verbose_name="Название")
    slug = AutoSlugField(populate_from="name", unique=True, verbose_name="Слаг")
    description = models.TextField(max_length=100, verbose_name="Описание")
    price = models.PositiveIntegerField(verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток")
    created = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    limited = models.BooleanField(default=False, verbose_name="Ограниченный тираж")
    specs = models.ManyToManyField("SpecName", through="Spec")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    sort_index = models.PositiveIntegerField(verbose_name="Индекс сортировки")
    purchases_num = models.PositiveIntegerField(
        default=0, verbose_name="Количество покупок", editable=False
    )
    free_delivery = models.BooleanField(
        default=False, verbose_name="Бесплатная доставка", editable=False
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        site_settings = SiteSettings.objects.first()
        if self.price >= site_settings.free_delivery_edge:
            self.free_delivery = True
        else:
            self.free_delivery = False
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.slug)])

    @property
    def reviews_count(self):
        return self.reviews.count()

    @property
    def is_stock(self):
        return self.stock > 0


class Category(models.Model):
    name = models.TextField(max_length=50, verbose_name="название категории")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
        verbose_name="Родительская категория",
    )
    slug = AutoSlugField(populate_from="name", unique=True, verbose_name="Слаг")
    icon = models.FileField(upload_to="cat_icons/", blank=True)
    image = models.ImageField(upload_to="cat_images/", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_min_product_price(self):
        products = Product.objects.filter(
            Q(category=self) | Q(category__parent=self), available=True
        )
        return products.aggregate(min_price=Min("price"))["min_price"]


class SpecName(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Имя характеристики"
        verbose_name_plural = "Имена характеристик"


class Spec(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="товар")
    spec_name = models.ForeignKey(
        SpecName, on_delete=models.CASCADE, verbose_name="Название"
    )
    value = models.CharField(max_length=50, verbose_name="Значение")

    def __str__(self):
        return f"{self.spec_name.name}: {self.value}"

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class Gallery(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/%Y/%m/%d")

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Reviews(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Продукт",
    )
    text = models.TextField(max_length=200, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.text
