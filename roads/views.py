from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Road
from .serializers import RoadSerializer
from django.db.models import OuterRef, Subquery, Value, Case, When, CharField
from readings.models import Reading
from django.conf import settings
from django.db.models import Count

# Create your views here.


class RoadViewSet(viewsets.ModelViewSet):
    serializer_class = RoadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        low_intensity = settings.LOW_INTENSITY
        medium_intensity = settings.MEDIUM_INTENSITY

        latest_speed_sq = (
            Reading.objects.filter(road=OuterRef("pk"))
            .order_by("-timestamp")
            .values("speed")[:1]
        )

        qs = Road.objects.annotate(
            latest_speed=Subquery(latest_speed_sq),
            intensity=Case(
                When(latest_speed__lte=20, then=Value("elevada")),
                When(latest_speed__lte=50, then=Value("média")),
                default=Value("baixa"),
                output_field=CharField(),
            ),
            readings_count=Count("readings"),
        )

        intensity_param = self.request.query_params.get("intensity")
        if intensity_param:
            qs = qs.filter(intensity=intensity_param)

        return qs
