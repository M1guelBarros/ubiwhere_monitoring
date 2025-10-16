from django.db import models
from django.utils import timezone

# Create your models here.


class Road(models.Model):
    # id = models.AutoField
    long_start = models.FloatField(default=0.0)
    lat_start = models.FloatField(default=0.0)
    long_end = models.FloatField(default=0.0)
    lat_end = models.FloatField(default=0.0)
    length = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Road: {self.id} - Speed: {self.speed}"
