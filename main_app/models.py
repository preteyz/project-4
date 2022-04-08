from django.db import models
from django.contrib.auth.models import User

# Create your models here.



ENVIRONMENT_CHOICES = (
    ("b", "beach"),
    ("m", "mountain"),
    ("c", "city"),
    ("r", "rural")
)


class TravelLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    img = models.CharField(max_length=250)
    environment = models.CharField(max_length=10, choices = ENVIRONMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    favorites = models.ManyToManyField(User, related_name='location_post')
    
    def total_faves(self):
        return self.favorites.count()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Review(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    rating = models.IntegerField()
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    travel_location= models.ForeignKey(TravelLocation, blank=True, on_delete=models.CASCADE) #move this to TravelLocations
    
    




