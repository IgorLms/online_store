from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models

from .managers import CustomUserManager


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserCustom(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField('email', max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Категории товаров')
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание категории')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название товара')
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.name


class HistoryChanges(models.Model):
    product = models.ForeignKey(Product, related_name="history", on_delete=models.CASCADE, verbose_name='Название товара')
    date_changes = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения товара')
    quantity_old = models.PositiveIntegerField(verbose_name='Количество товара до изменения')
    quantity_now = models.PositiveIntegerField(verbose_name='Количество товара после изменения')

    def __str__(self):
        return f'{self.product}'