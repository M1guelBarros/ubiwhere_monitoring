from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from roads.views import RoadViewSet
from sensors.views import SensorViewSet

router = DefaultRouter()
router.register(r"roads", RoadViewSet, basename="roads")
router.register(r"sensors", SensorViewSet, basename="sensors")
urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
]
