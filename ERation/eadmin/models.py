from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
# Create your models here.

# Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )

        print(password)
        user.is_staff = True
        user.admin = True
        user.role = 'admin'
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    CHOICES = (
        ('admin', 'Admin'),
        ('shop', 'Shop'),
        ('staff', 'Delivery Staff'),
    )

    email = models.CharField(
        verbose_name='Email ID',
        name='email',
        unique=True,
        max_length=100,
        validators=(
            EmailValidator(message='Invalid Email'),
        )
    )

    role = models.CharField(
        verbose_name='User Role',
        name='role',
        max_length=10,
        default='shop',
        choices=CHOICES,
        blank=False
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email


class Cards(models.Model):
    name = models.CharField(
        verbose_name='Card Name',
        name='card_name',
        max_length=20,
        unique=True,
        help_text="This cannot be changed in future",
        validators=(
            MinLengthValidator(5),
            MaxLengthValidator(20)
        )
    )

    def __str__(self):
        return self.card_name


class Products(models.Model):
    CHOICES = (
        ('kg', 'Kilogram'),
        ('ltr', 'Liter'),
    )
    name = models.CharField(
        name='name',
        verbose_name='Product name',
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(20)
        ]
    )
    unit = models.CharField(
        name='unit',
        verbose_name='Unit(s)',
        max_length=10,
        choices=CHOICES
    )
    details = models.CharField(
        name='details',
        verbose_name='Details',
        max_length=250,
        default='No details are available',
        validators=[
            MaxLengthValidator(250)
        ]
    )
    price = models.IntegerField(
        name='price',
        verbose_name='Price',
        default=0,
        validators=[
            MinValueValidator(0, "Invalid price"),
            MaxValueValidator(1000, "Invalid price")
        ]
    )
    def __str__(self):
        return self.name


class Allocations(models.Model):
    class Meta:
        unique_together = ('card_name', 'product')

    card_name = models.ForeignKey(
        to=Cards,
        to_field='card_name',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        to=Products,
        to_field='name',
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        name='quantity',
        default=1, 
        help_text="Units will be automatically computed",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )


class SalesReport(models.Model):

    class Meta:
        pass
        #unique_together = ('shop_id', 'customer_id', 'product', 'month')

    YEAR = datetime.now().year
    MONTH = datetime.now().month
    DAY = datetime.now().day

    shop_id = models.ForeignKey(
        to='shop.Shop',
        to_field='shop_id',
        on_delete=models.CASCADE
    )
    customer_id = models.ForeignKey(
        to='customer.Customer',
        to_field='card_number',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to=Products,
        to_field='name',
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        name='quantity',
        verbose_name='Quantity',
        help_text='Units will be automatically computed',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    year = models.IntegerField(
        verbose_name='year',
        blank=False,
        default=YEAR,
        editable=False
    )
    month = models.CharField(
        max_length=20,
        verbose_name='month',
        blank=False,
        default=MONTH,
        editable=False
    )
    day = models.CharField(
        max_length=5,
        verbose_name='Day',
        blank=False,
        default=DAY,
        editable=False
    )

class Complaints(models.Model):

    customer = models.ForeignKey(
        to='customer.Customer',
        on_delete=models.CASCADE
    )
    date_posted = models.DateField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )
    title = models.CharField(
        max_length=100,
        null=False,
        validators=[MinLengthValidator(10, "Please provide a longer title")]
    )
    complaint = models.TextField(
        max_length=2000,
        null=False,
        validators=[MinLengthValidator(10, "Explain your issue in atleast 10 chars")]
    )
    reply = models.TextField(
        max_length=2000,
        null=False,
        validators=[MinLengthValidator(10, "Write your reply in atleast 10 chars")]
    )
    def __str__(self):
        return self.customer.card_number
