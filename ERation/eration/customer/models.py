from django.db import models
from django.core import validators as v
import eadmin.models as admin

# Create your models here.
class Customer(models.Model):   
    name = models.CharField(
        verbose_name='Name',
        name='name',
        max_length=50,
        null=False,
        validators=(
            v.MinLengthValidator(3),
        )
    )

    phone = models.CharField(
        verbose_name='Phone',
        name='phone',
        unique=True,
        null=False,
        max_length=10,
        validators=(
            v.MinLengthValidator(10),
            v.MaxLengthValidator(10)
        )
    )

    address = models.CharField(
        verbose_name="Address",
        name='address',
        blank=False,
        max_length=150,
        validators=(
            v.MinLengthValidator(10),
            v.MaxLengthValidator(150)
        )
    )

    card_number = models.CharField(
        verbose_name="Ration card number",
        name='card_number',
        blank=False,
        max_length=50,
        unique=True,
        validators=(
            v.MinLengthValidator(10),
            v.MaxLengthValidator(15)
        )
    )

    shop_id = models.ForeignKey(
        to='shop.Shop',
        to_field='shop_id',
        on_delete=models.CASCADE
    )

    card_type = models.ForeignKey(
        verbose_name='Card type',
        name='card_type',
        max_length=10,
        blank=False,
        to='eadmin.Cards',
        to_field='card_name',
        on_delete=models.CASCADE
    )
    email = models.CharField(
        max_length=50,
        verbose_name='Email',
    )
    aadhar = models.BigIntegerField(
        verbose_name='Aadhar Number',
        validators=[
            v.MinValueValidator(111111111111),
            v.MaxValueValidator(9999999999999999)
        ]
    )
class Orders(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Delivered', 'Delivered'),
        ('Rejected', 'Rejected'),
        ('Out for delivery', 'Out for delivery')
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'eadmin.Products',
        on_delete=models.CASCADE
    )
    price=models.IntegerField(
        verbose_name='Price',
        default=0,
        validators=[
            v.MaxValueValidator(10000, 'Price cannot exceed 10000'),
            v.MinValueValidator(0, 'The minimum price should be 0')
        ]
    )
    day=models.IntegerField(
        verbose_name='Day',
        blank=False,
    )
    month=models.IntegerField(
        verbose_name='Month',
        blank=False
    )
    year=models.IntegerField(
        verbose_name='Year',
        blank=False
    )
    dday=models.IntegerField(
        verbose_name='Day',
        blank=False,
        default=0
    )
    dmonth=models.IntegerField(
        verbose_name='Month',
        blank=False,
        default=0
    )
    dyear=models.IntegerField(
        verbose_name='Year',
        blank=False,
        default=0
    )
    otp=models.IntegerField(
        verbose_name='OTP',
        validators=[
            v.MinValueValidator(0, "Invalid OTP Value"),
            v.MaxValueValidator(9999, "Invalid OTP")
        ]
    )
    status=models.CharField(
        choices=STATUS,
        max_length=50
    )
    delivery_staff=models.CharField(
        max_length=50,
        verbose_name = 'Delivery Staff',
        default = "0",
    )
    quantity=models.IntegerField(
        verbose_name='Quantity',
        default=1
    )