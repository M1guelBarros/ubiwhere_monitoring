from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from roads.views import RoadViewSet
from sensors.views import SensorViewSet
from readings.views import ReadingViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()
router.register(r"roads", RoadViewSet, basename="roads")
router.register(r"sensors", SensorViewSet, basename="sensors")
router.register(r"readings", ReadingViewSet, basename="readings")
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
