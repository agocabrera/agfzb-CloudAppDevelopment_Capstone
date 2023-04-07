from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_types = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        ("SPORT", "Sport")
    ]

    name = models.CharField(max_length=30)
    make = models.ForeignKey(CarMake, on_delete=models.DO_NOTHING)
    year = models.DateField()
    type = models.CharField(max_length=30, choices=car_types)
    dealer_id = models.IntegerField()

    def __str__(self):
        return self.name


class CarDealer:
    def __init__(self, id, city, st, address, zip, lat, long, short_name, full_name):
        self.id = id
        self.city = city
        self.st = st
        self.address = address
        self.zip = zip
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self, id, name, dealership, review, purchase, purchase_date=None,
                 car_make=None, car_model=None, car_year=None, sentiment=None):
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Review name: " + self.name
