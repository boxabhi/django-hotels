from django.db import models

# Create your models here.


class Emenities(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    


class Hotels(models.Model):
    hotel_name = models.CharField(max_length=100)
    hotel_description = models.TextField()
    price = models.IntegerField()
    image = models.CharField(max_length=500)
    emenities = models.ManyToManyField(Emenities)
    
    
    def __str__(self):
        return self.hotel_name    
    
from geopy.geocoders import Nominatim 
from math import radians, cos, sin, asin, sqrt
  
class Pincode(models.Model):
    pincode = models.CharField(max_length=100)
    lat = models.FloatField(null=True , blank=True)
    lon = models.FloatField(null=True , blank=True)
    
    def save(self, *args, **kwargs): 
        geolocator = Nominatim(user_agent="geoapiExercises")
        zipcode = self.pincode
        location = geolocator.geocode(zipcode)
        self.lat = location.latitude
        self.lon = location.longitude
        super(Pincode, self).save(*args, **kwargs) 
    
    

    def distance(self, lat2, long2):
        lat1, long1, lat2, long2 = map(radians, [self.lat, self.lon, lat2, long2])
        dlon = long2 - long1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371* c    
        return km

    def call(self):
        print(self.pincode)
    