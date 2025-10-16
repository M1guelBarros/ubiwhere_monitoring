from rest_framework import viewsets
from .models import Road
from .serializers import RoadSerializer

# Create your views here.


class RoadViewSet(viewsets.ModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadSerializer
