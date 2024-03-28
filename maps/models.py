from django.db import models
# from django.contrib.auth.models import User
# Create your models here.

# class Profile(models.Model):
#     user            = models.OneToOneField(User, on_delete=models.PROTECT, related_name="profile")
#     picture         = models.CharField(max_length=200) #holds a link to google url. 

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


# a model for each of the "tags" made. This will simply be a way of providing
# the user's location to the server. 
class Tag(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    x_pos = models.FloatField(null=True, blank=True)
    y_pos = models.FloatField(null=True, blank=True)

    rotation = models.FloatField(null=True, blank=True)

    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        related_name="tags",
        null=True
    )

    last_update_time = models.FloatField(null=True, blank=True)