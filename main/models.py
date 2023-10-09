from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField


class User(AbstractUser):
    email = models.EmailField(
        _("email address"), unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    property_description = models.TextField(max_length=900)
    price = models.PositiveIntegerField()
    phone = models.CharField(max_length=25)

    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PropertyAddress(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=20)
    latitude = models.CharField(max_length=15)
    longitude = models.CharField(max_length=15)


APPLIANCES = (
    ('Dishwasher', 'Dishwasher'), ('Dryer', 'Dryer'),
    ('Freezer', 'Freezer'), ('Garbage disposal', 'Garbage disposal'),
    ('Microwave', 'Microwave'), ('Range / Oven', 'Range / Oven'),
    ('Refrigerator', 'Refrigerator'), ('Trash compactor', 'Trash compactor'),
    ('Washer', 'Washer'),
)

FLOOR_COVERING = (
    ('Carpet', 'Carpet'), ('Concrete', 'Concrete'),
    ('Hardwood', 'Hardwood'), ('Laminate', 'Laminate'),
    ('Slate', 'Slate'), ('Softwood', 'Softwood'),
    ('Tile', 'Tile'), ('Linoleum / Vinyl', 'Linoleum / Vinyl'),
    ('Other', 'Other'),
)

COOLING_TYPE = (
    ('Central', 'Central'), ('Evaporative', 'Evaporative'),
    ('Refrigeration', 'Refrigeration'), ('Geothermal', 'Geothermal'),
    ('Solar', 'Solar'), ('Wall', 'Wall'),
    ('Other', 'Other'), ('None', 'None'),
)

HEATING_TYPE = (
    ('Electric', 'Electric'), ('Forced air', 'Forced air'),
    ('Heat pump', 'Heat pump'), ('Geothermal', 'Geothermal'),
    ('Radiant', 'Radiant'), ('Stove', 'Stove'),
    ('Gas', 'Gas'), ('Solar', 'Solar'),
    ('Wall', 'Wall'), ('Other', 'Other'),
)

ROOMS = (
    ('Dining room', 'Dining room'), ('Family room', 'Family room'),
    ('Laundry room', 'Laundry room'), ('Master bath', 'Master bath'),
    ('Mud room', 'Mud room'), ('Office', 'Office'),
    ('Pantry', 'Pantry'), ('Workshop', 'Workshop'),
    ('Recreation room', 'Recreation room'), ('Walk-in closet', 'Walk-in closet'),
)

OUTDOOR_AMENITIES = (
    ('Balcony / patio', 'Balcony / patio'), ('Barbecue area', 'Barbecue area'),
    ('Deck', 'Deck'), ('Dock', 'Dock'),
    ('Fenced yard', 'Fenced yard'), ('Garden', 'Garden'),
    ('Greenhouse', 'Greenhouse'), ('Spa / hot tub', 'Spa / hot tub'),
    ('Lawn', 'Lawn'), ('Pond', 'Pond'),
    ('Pool', 'Pool'), ('Porch', 'Porch'),
)

PARKING = (
    ('Carport', 'Carport'), ('Garage-attached', 'Garage-attached'),
    ('Garage-detached', 'Garage-detached'), ('Off-street', 'Off-street'),
    ('On-street', 'On-street'), ('None', 'None'),
)

VIEW = (
    ('City', 'City'), ('Mountain', 'Mountain'),
    ('Park', 'Park'), ('Territorial', 'Territorial'),
    ('Water', 'Water'), ('None', 'None'),
)

class PropertyAmenities(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    appliances = MultiSelectField(choices=APPLIANCES, blank=True, max_length=108, default='')
    floor_covering = MultiSelectField(choices=FLOOR_COVERING, blank=True, max_length=84, default='')
    cooling_type = MultiSelectField(choices=COOLING_TYPE, blank=True, max_length=72, default='')
    heating_type = MultiSelectField(choices=HEATING_TYPE, blank=True, max_length=84, default='')
    rooms = MultiSelectField(choices=ROOMS, blank=True, max_length=119, default='')
    outdoor_amenities = MultiSelectField(choices=OUTDOOR_AMENITIES, blank=True, max_length=119, default='')
    parking = MultiSelectField(choices=PARKING, blank=True, max_length=72, default='')
    view = MultiSelectField(choices=VIEW, blank=True, max_length=72, default='')


property_choises = [
        (None, 'Select house type'),
        ('Appartment', 'Appartment'),
        ('Single Family House', 'Single Family House'),
        ('Condominium', 'Condominium'),
        ('Townhouse', 'Townhouse'),
        ('Mobile Home / Manufactured Home', 'Mobile Home / Manufactured Home')
    ]

bedrooms_choises = [
    (None, 'Select bedrooms'),
    ('Studio', 'Studio'),
    ('1 bed', '1 bed'),
    ('2 bed', '2 bed'),
    ('3 bed', '3 bed'),
    ('4 bed+', '4 bed+')
]

bathrooms_choises = [
    (None, 'Select bathrooms'),
    ('1 bath', '1 bath'),
    ('1.5 bath', '1.5 bath'),
    ('2 bath', '2 bath'),
    ('2.5 bath', '2.5 bath'),
    ('3 bath', '3 bath'),
    ('3.5 bath', '3.5 bath'),
    ('4 bath+', '4 bath+')
]
class PropertyInfo(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=31, choices=property_choises, default='')
    bedrooms = models.CharField(max_length=6, choices=bedrooms_choises, default='')
    bathrooms = models.CharField(max_length=8, choices=bathrooms_choises, default='')
    square_footage = models.PositiveIntegerField()
    HOA_dues = models.PositiveIntegerField(blank=True, null=True)
    lease_terms = models.TextField(max_length=600)


class PropertyImages(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='photos/%Y/%m/%d')

    def __str__(self):
        return self.property.user.email

class PropertyAddUnit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    title_unit = models.CharField(max_length=100)
    bedrooms_unit = models.CharField(max_length=6, choices=bedrooms_choises, default='')
    bathrooms_unit = models.CharField(max_length=8, choices=bathrooms_choises, default='')
    square_footage_unit = models.PositiveIntegerField()
    price_unit = models.PositiveIntegerField()
    image_unit = models.ImageField(upload_to='photos/%Y/%m/%d')

