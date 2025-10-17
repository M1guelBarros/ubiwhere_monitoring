from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Road
from .serializers import RoadSerializer
from django.db.models import OuterRef, Subquery
from readings.models import Reading

# Create your views here.


class RoadViewSet(viewsets.ModelViewSet):
    serializer_class = RoadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        latest_speed = (
            Reading.objects.filter(road=OuterRef("pk"))
            .order_by("-timestamp")
            .values("speed")[:1]
        )
        return Road.objects.annotate(speed=Subquery(latest_speed))
