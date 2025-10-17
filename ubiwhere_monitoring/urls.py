from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from roads.views import RoadViewSet
from sensors.views import SensorViewSet
from readings.views import ReadingViewSet

router = DefaultRouter()
router.register(r"roads", RoadViewSet, basename="roads")
router.register(r"sensors", SensorViewSet, basename="sensors")
router.register(r"readings", ReadingViewSet, basename="readings")
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
]
