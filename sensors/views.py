from rest_framework import viewsets
from .models import Sensor
from .serializers import SensorSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
