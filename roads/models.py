from django.db import models

# Create your models here.


class Roads(models.Model):
    id = models.AutoField
    long_start = models.FloatField
    lat_start = models.FloatField
    long_end = models.FloatField
    lat_end = models.FloatField
    length = models.FloatField
    speed = models.FloatField

    def __str__(self):
        return f"Road: {self.id} - Speed: {self.speed}"
