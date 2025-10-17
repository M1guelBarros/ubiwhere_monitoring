from rest_framework import serializers
from .models import Road


class RoadSerializer(serializers.ModelSerializer):

    intensity = serializers.SerializerMethodField()

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
        ]

    def get_intensity(self, obj):
        speed = getattr(obj, "speed", None)
        if speed is None:
            return None
        if obj.speed <= 20:
            return "elevada"
        elif obj.speed <= 50:
            return "média"
        else:
            return "baixa"
