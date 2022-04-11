from django.db import models
from django.contrib.auth.models import User

# Create your models here.



ENVIRONMENT_CHOICES = (
    ("beach", "beach"),
    ("mountain", "mountain"),
    ("city", "city"),
    ("rural", "rural")
)

# favorites = models.ManyToManyField(Review)
class TravelLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    img = models.CharField(max_length=250)
    environment = models.CharField(max_length=10, choices = ENVIRONMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
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
    
    def __str__(self):
        return self.name
    




