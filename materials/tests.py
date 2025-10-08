from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.course = Course.objects.create(name='testCourse1', owner=self.user)
        self.lesson = Lesson.objects.create(name='testLesson1', url_video='test_url/youtube.com/test', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lessons_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse('materials:lessons_create')
        data = {
            'name': 'testLesson2',
            'url_video': 'test_url2/youtube.com',
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse('materials:lessons_update', args=(self.lesson.pk,))
        data = {
            'name': 'testLesson1update',
            'url_video': 'test_url_update/youtube.com',
            'course': self.course.pk
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), 'testLesson1update'
        )

    def test_lesson_delete(self):
        url = reverse('materials:lessons_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('materials:lessons_list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.pk,
                    'url_video': self.lesson.url_video,
                    'name': self.lesson.name,
                    'description': None,
                    'preview_image': None,
                    'course': self.course.pk,
                    'owner': self.user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.course = Course.objects.create(name='testCourse1', owner=self.user)
        self.lesson = Lesson.objects.create(
            name='testLesson1',
            url_video='test_url/youtube.com/test',
            course=self.course,
            owner=self.user
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            is_active=True
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.course.name
        )

    def test_course_create(self):
        url = reverse('materials:course-list')
        data = {
            'name': 'testCourse2'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        data = {
            'name': 'testCourse1update',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), 'testCourse1update'
        )

    def test_course_delete(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse('materials:course-list')
        response = self.client.get(url)
        data = response.json()
        print(data)
        result = [{
            'id': self.course.pk,
            'is_subscribed': True,
            'name': self.course.name,
            'description': None,
            'preview_image': None,
            'owner': self.user.pk
        }]
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )