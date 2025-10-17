from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Reading
from .serializers import ReadingSerializer

# Create your views here.


class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all().select_related("road")
    serializer_class = ReadingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
