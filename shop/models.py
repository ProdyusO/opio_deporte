"""Model's module."""
# pylint: disable=R0903, W0221
from django.db import models
from .utilities import validation_phone_number  # pylint: disable=E0402


class Product(models.Model):
    """Goods list model."""

    title = models.CharField(max_length=20, verbose_name="Товар")
    image = models.ImageField(verbose_name="Головне Фото")
    image2 = models.ImageField(blank=True, verbose_name="Друге Фото")
    image3 = models.ImageField(blank=True, verbose_name="Третьє Фото")
    image4 = models.ImageField(blank=True, verbose_name="Четверте Фото")
    content = models.TextField(blank=True, verbose_name="Опис товару")
    price = models.FloatField(null=True, blank=True, verbose_name="Ціна")
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="category",
        verbose_name="Категорія",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Опубликовано"
    )

    def __str__(self):
        """Shows object's name."""
        return str(self.title)

    class Meta:
        """Product's model settings."""

        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ["-created_at"]


class Category(models.Model):
    """Categories list model."""

    title = models.CharField(max_length=20, verbose_name="Категорія")

    def __str__(self):
        """Shows category name."""
        return str(self.title)

    class Meta:
        """Categories model settings."""

        verbose_name = "Категорію"
        verbose_name_plural = "Категорії"
        ordering = ["title"]


class CartProduct(models.Model):
    """Customer's items."""

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name="Продукт"
    )
    price = models.DecimalField(max_digits=9, decimal_places=1, verbose_name="Ціна")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Кількість")
    total = models.DecimalField(max_digits=9, decimal_places=1, verbose_name="Вартість")
    in_order = models.BooleanField(default=False, verbose_name="Оформлено")
    done = models.BooleanField(
        default=False, null=True, blank=True, verbose_name="Заказ виконаний"
    )
    customer = models.ForeignKey(
        "Customer", on_delete=models.PROTECT, verbose_name="Клієнт"
    )
    created = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name="Активність"
    )

    def __str__(self):
        """Shows customer."""
        return str(self.customer)

    def save(self, **kwargs):
        """Pre-save settings."""
        self.total = self.price * self.quantity
        return super().save(**kwargs)

    class Meta:
        """CartProduct's model settings."""

        verbose_name = "Продукт кошику"
        verbose_name_plural = "Продукти кошика"


class Customer(models.Model):
    """Customer's list."""

    BUYING_TYPE_SELF = "Самовивіз"
    BUYING_TYPE_DELIVERY = "Доставка"

    BUYING_TYPE_CHOICES = {
        (BUYING_TYPE_SELF, "Самовивіз, м. Одеса, вул. Преображенська 34"),
        (BUYING_TYPE_DELIVERY, "Доставка Новою Поштою"),
    }
    name = models.CharField(max_length=20, verbose_name="Кліент")
    first_name = models.CharField(max_length=10, verbose_name="Ім'я")
    last_name = models.CharField(max_length=10, verbose_name="Прізвище")
    email = models.EmailField(blank=True, verbose_name="e-mail")
    phone_number = models.CharField(
        max_length=10, validators=[validation_phone_number], verbose_name="Телефон"
    )
    buying_type = models.CharField(
        max_length=100,
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF,
        verbose_name="Тип замовлення",
    )
    new_post = models.CharField(
        max_length=50, blank=True, verbose_name="Місто та номер почтового відділення"
    )
    comment = models.TextField(
        blank=True, null=True, verbose_name="Додати коментар до замовлення"
    )
    created = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name="Активність"
    )

    def __str__(self):
        """Shows customer's name."""
        return str(self.name)

    class Meta:
        """Customer's model settings."""

        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"
