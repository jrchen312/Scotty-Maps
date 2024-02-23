from django.db import models

# Create your models here.


# Model for classes
class Location(models.Model):

    # name
    name = models.CharField(max_length=100)

    # latitude and longitude of the location
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return f"{self.name}"


# Model for each floor that belongs to each location
class Floor(models.Model):
    # corresponding location 
    location = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE,
        related_name="floors"
    )

    # floor name
    name = models.CharField(max_length=100)

    # image path
    img_path = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.location.name} {self.name}"


