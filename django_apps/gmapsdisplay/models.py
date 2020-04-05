from django.db import models
import json
import geopy

# Create your models here.


class DeliveryRoute(models.Model):
    delivery_date = models.DateField()

    def getshortestpath(self):
        #feed to routific api
        pass

class Order(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    delivery_tour = models.ForeignKey(DeliveryRoute, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    def convert_to_coordinates(self):
        address = u'%s %s' % (self.city, self.address)
        try:
           locator = geopy.Nominatim(user_agent="myGeocoder")
           location = locator.geocode(address)
        except (ValueError):
            pass
        
        return location

