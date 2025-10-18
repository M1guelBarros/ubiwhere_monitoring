from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from roads.models import Road
from .models import Reading

User = get_user_model()


class ReadingsTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "", "pass")
        self.road = Road.objects.create(
            long_start=1.0, lat_start=1.0, long_end=2.0, lat_end=2.0, length=1.0
        )
        self.reading = Reading.objects.create(road=self.road, speed=61)

    def test_anonymous_get_readings(self):
        url = reverse("readings-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_post_readings(self):
        url = reverse("readings-list")
        response = self.client.post(url, {"road": self.road.id, "speed": 50})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_delete_readings(self):
        url = reverse("readings-detail", args=[self.reading.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_put_reading(self):
        url = reverse("readings-detail", args=[self.reading.id])
        data = {"road": self.road.id, "speed": 99}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_post_readings(self):
        self.client.login(username="admin", password="pass")
        url = reverse("readings-list")
        response = self.client.post(url, {"road": self.road.id, "speed": 84})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_delete_readings(self):
        self.client.login(username="admin", password="pass")
        url = reverse("readings-detail", args=[self.reading.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_put_reading(self):
        self.client.login(username="admin", password="pass")
        url = reverse("readings-detail", args=[self.reading.id])
        data = {"road": self.road.id, "speed": 99}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
