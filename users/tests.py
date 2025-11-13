from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.other_user = User.objects.create(email="other@test.com")
        self.course = Course.objects.create(name="testCourse1", owner=self.user)

        self.client.force_authenticate(user=self.user)

    def test_update_subscription_on_course(self):
        url = reverse("materials:subscription")
        payload = {"course_id": self.course.pk}
        response = self.client.post(url, payload)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("message"), "Подписка добавлена")
        second_response = self.client.post(url, payload)
        second_data = second_response.json()
        self.assertEqual(second_data.get("message"), "Подписка удалена")
