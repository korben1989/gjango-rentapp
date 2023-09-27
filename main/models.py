from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(
        _("email address"), unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

class AddPropertyGoogle(models.Model):
    property_choises = [
        ('Appartment', 'Appartment'),
        ('Single Family House', 'Single Family House'),
        ('Condominium', 'Condominium'),
        ('Townhouse', 'Townhouse'),
        ('Mobile Home / Manufactured Home', 'Mobile Home / Manufactured Home')
    ]

    location = models.CharField(max_length=600, blank=False)
    apartment_unit = models.CharField(max_length=50, blank=False)
    # total_units_in_the_building = models.IntegerField(blank=False)
    property_type = models.CharField(max_length=31, choices=property_choises, default='')
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)

    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.location

# class PropertyInfo(models.Model):
#     property = models.ForeignKey(AddPropertyGoogle, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     price = models.PositiveIntegerField()
#     description = models.TextField()


class PropertyImages(models.Model):
    image = models.ImageField(upload_to='photos/%d/%m/%Y')
    property = models.ForeignKey(AddPropertyGoogle, on_delete=models.CASCADE)

    def __str__(self):
        return self.property.user.email

