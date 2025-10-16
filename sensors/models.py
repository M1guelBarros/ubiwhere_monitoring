from django.db import models

# Create your models here.


class Sensor(models.Model):
    # id = models.AutoField
    name = models.CharField(max_length=200)
    uuid = models.UUIDField(unique=True)

    def __str__(self):
        return f"Sensor {self.name}"
