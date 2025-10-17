from django.db import models
from roads.models import Road


class Reading(models.Model):
    road = models.ForeignKey(
        Road,
        on_delete=models.CASCADE,
        related_name="readings",
    )
    speed = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Reading On Road={self.road_id}, Speed={self.speed} at {self.timestamp}"
