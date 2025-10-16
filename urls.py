from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from roads.views import RoadViewSet

router = DefaultRouter()
router.register("roads/", RoadViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("admi/", admin.site.urls),
]
