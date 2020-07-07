from django.db import models
from django.core import validators as v
from eadmin.models import User
from shop.models import Shop

# Create your models here.
class DeliveryStaff(models.Model):
    id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    shop = models.ForeignKey(
        to=Shop,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name='Staff Name',
        name='name',
        blank=False,
        max_length=100
    )

    staff_id = models.CharField(
        verbose_name='Staff Id',
        name='staff_id',
        max_length=20,
        unique=True,
        blank=False
    )

    address = models.CharField(
        verbose_name='Address',
        name='address',
        max_length=20,
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
