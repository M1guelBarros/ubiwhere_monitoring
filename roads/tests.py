from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Road
from readings.models import Reading

User = get_user_model()


class RoadsTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "", "pass")
        self.road = Road.objects.create(
            long_start=1.0, lat_start=1.0, long_end=2.0, lat_end=2.0, length=1.0
        )

    def test_anonymous_get_road(self):
        url = reverse("roads-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_post_road(self):
        url = reverse("roads-list")
        response = self.client.post(
            url,
            {
                "long_start": 1.0,
                "lat_start": 1.0,
                "long_end": 2.0,
                "lat_end": 2.0,
                "length": 1.0,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_delete_road(self):
        url = reverse("roads-detail", args=[self.road.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_put_road(self):
        url = reverse("roads-detail", args=[self.road.id])
        data = {
            "long_start": 5.0,
            "lat_start": 5.0,
            "long_end": 5.0,
            "lat_end": 5.0,
            "length": 5.3,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_post_road(self):
        self.client.login(username="admin", password="pass")
        url = reverse("roads-list")
        response = self.client.post(
            url,
            {
                "long_start": 9,
                "lat_start": 9,
                "long_end": 10,
                "lat_end": 10,
                "length": 30,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_delete_roads(self):
        self.client.login(username="admin", password="pass")
        url = reverse("roads-detail", args=[self.road.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_put_road(self):
        self.client.login(username="admin", password="pass")
        url = reverse("roads-detail", args=[self.road.id])
        data = {
            "long_start": 5.0,
            "lat_start": 5.0,
            "long_end": 5.0,
            "lat_end": 5.0,
            "length": 5.3,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_last_intensity(self):
        Reading.objects.create(road=self.road, speed=10)
        Reading.objects.create(road=self.road, speed=40)
        Reading.objects.create(road=self.road, speed=60)
        response = self.client.get(reverse("roads-detail", args=[self.road.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["intensity"], "baixa")
