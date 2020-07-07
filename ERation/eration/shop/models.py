from django.db import models
from django.core import validators as v
from eadmin.models import User

# Create your models here.
class Shop(models.Model):
    id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    name = models.CharField(
        verbose_name='Shop Name',
        name='name',
        blank=False,
        max_length=100
    )

    shop_id = models.CharField(
        verbose_name='Shop Id',
        name='shop_id',
        max_length=20,
        unique=True,
        blank=False
    )

    address = models.CharField(
        verbose_name='Address',
        name='address',
        max_length=100,
        blank=False
    )

    phone = models.CharField(
        verbose_name='Phone',
        name='phone',
        max_length=10,
        unique=True,
        blank=False,
        validators=(
            v.MinLengthValidator(10),
            v.MaxLengthValidator(10)
        )
    )

    pin = models.CharField(
        verbose_name='PIN',
        name='pin',
        max_length=6,
        blank=False,
        validators=(
            v.MinLengthValidator(6),
            v.MaxLengthValidator(6)
        )
    )

    place = models.CharField(
        verbose_name='Place',
        name='place',
        max_length=50,
        blank=False,
        help_text='Please enter nearby town or place',
        validators=(
            v.MinLengthValidator(5),
            v.MaxLengthValidator(50)
        )
    )

    def __str__(self):
        return self.name

class StockUpdates(models.Model):
    date = models.DateField(
        verbose_name='Date',
        auto_now_add=True,
    )
    shop_id = models.ForeignKey(
        to='shop.Shop',
        on_delete=models.CASCADE,
        blank=False
    )
    name = models.CharField(
        max_length = 20,
        verbose_name = 'Name',
        blank=False
    )

class Stocks(models.Model):
    shop_id = models.ForeignKey(
        to='shop.Shop',
        on_delete=models.CASCADE,
    )
    update_id = models.ForeignKey(
        to='shop.StockUpdates',
        on_delete=models.CASCADE,
        verbose_name='Stock Update ID',
    )
    product = models.ForeignKey(
        to='eadmin.Products',
        on_delete=models.CASCADE
    )
    quantity =models.IntegerField(
        verbose_name='Quantity',
        help_text='Please enter the new stock',
        default=0
    )