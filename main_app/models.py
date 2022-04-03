from django.db import models
from django.contrib.auth.models import User

# Create your models here.



ENVIRONMENT_CHOICES = (
    ("b", "beach"),
    ("m", "mountain"),
    ("c", "city"),
    ("r", "rural")
)


class Review(models.Model):
    createdby = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

# favorites = models.ManyToManyField(Review)
class TravelLocation(models.Model):
    createdby = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    img = models.CharField(max_length=250)
    environment = models.CharField(max_length=10, choices = ENVIRONMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    Review = models.ForeignKey(Review, on_delete=models.CASCADE) #move this to TravelLocations
    
    
def __str__(self):
    return self.name


def __str__(self):
    return self.name

class Meta:
    ordering = ['name']

