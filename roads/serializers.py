from rest_framework import serializers
from .models import Road


class RoadSerializer(serializers.ModelSerializer):

    intensity = serializers.CharField()
    readings_count = serializers.IntegerField()

    class Meta:
        model = Road
        fields = [
            "id",
            "long_start",
            "long_end",
            "lat_start",
            "lat_end",
            "length",
            "updated_time",
            "intensity",
            "readings_count",
        ]
