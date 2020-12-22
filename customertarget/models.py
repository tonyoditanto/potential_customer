from django.db import models

# Create your models here.


class CustomerPotential(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=300)
    customer_type = models.CharField(max_length=50)
    keyword = models.CharField(max_length=50)
    radius = models.CharField(max_length=20)
    place_id = models.CharField(max_length=200)
    latitude_origin = models.FloatField(max_length=30)
    longitude_origin = models.FloatField(max_length=30)
    latitude_destination = models.FloatField(max_length=30)
    longitude_destination = models.FloatField(max_length=30)
    phone_number = models.CharField(max_length=20)
    distance_driving = models.FloatField(max_length=100)
