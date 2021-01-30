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
    
    