from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.anonymous_user = None
        self.user = User.objects.create(email='test@test.com')
        self.owner_user = User.objects.create(email='owner@test.com')
        self.moder_user = User.objects.create(email='moder@test.com')
        moder_group, created = Group.objects.get_or_create(name="Модераторы")
        self.moder_user.groups.add(moder_group)

        self.course = Course.objects.create(name='testCourse1', owner=self.user)
        self.lesson = Lesson.objects.create(name='testLesson1', url_video='test_url/youtube.com/test', course=self.course, owner=self.user)
        self.lesson_owner = Lesson.objects.create(name='testLesson1_owner', url_video='test_url/youtube.com/test', course=self.course, owner=self.owner_user)

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
            Lesson.objects.all().count(), 3
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
            Lesson.objects.all().count(), 1
        )

    def test_lesson_list(self):
        url = reverse('materials:lessons_list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 2,
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
                },
                {
                    'id': self.lesson_owner.pk,  # ← второй урок
                    'url_video': self.lesson_owner.url_video,
                    'name': self.lesson_owner.name,
                    'description': None,
                    'preview_image': None,
                    'course': self.course.pk,
                    'owner': self.owner_user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

    def test_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)

        # Редактирование своего урока - разрешено
        url = reverse('materials:lessons_update', args=(self.lesson_owner.pk,))
        data = {'name': 'Updated Lesson'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Редактирование чужого урока - запрещено
        url = reverse('materials:lessons_update', args=(self.lesson.pk,))
        data = {'name': 'Updated Lesson'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_access(self):
        self.client.force_authenticate(user=self.moder_user)

        # Создание урока - запрещено
        url = reverse('materials:lessons_create')
        data = {
            'name': 'testLesson2',
            'url_video': 'test_url2/youtube.com',
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Просмотр любого урока - разрешен
        url = reverse('materials:lessons_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Редактирование чужого урока - разрешено
        url = reverse('materials:lessons_update', args=(self.lesson.pk,))
        data = {'name': 'Moder Updated'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.owner_user = User.objects.create(email='owner@test.com')
        self.moder_user = User.objects.create(email='moder@test.com')
        moder_group, created = Group.objects.get_or_create(name="Модераторы")
        self.moder_user.groups.add(moder_group)

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

    def test_course_other_access_matrix(self):
        test_cases = [
            # (user, action, expected_status)
            (None, 'create', status.HTTP_401_UNAUTHORIZED),  # аноним
            (self.owner_user, 'create', status.HTTP_201_CREATED),  # владелец
            (self.moder_user, 'create', status.HTTP_403_FORBIDDEN),  # модератор

            (None, 'retrieve', status.HTTP_401_UNAUTHORIZED),  # аноним
            (self.user, 'retrieve', status.HTTP_200_OK),  # владелец в данном случае
            (self.owner_user, 'delete', status.HTTP_403_FORBIDDEN),  # сторонний пользователь в данном случае
            (self.moder_user, 'retrieve', status.HTTP_200_OK),  # модератор

            (None, 'update', status.HTTP_401_UNAUTHORIZED),  # аноним
            (self.owner_user, 'update', status.HTTP_200_OK),  # владелец
            (self.moder_user, 'update', status.HTTP_200_OK),  # модератор

            (None, 'delete', status.HTTP_401_UNAUTHORIZED),  # аноним
            (self.owner_user, 'delete', status.HTTP_403_FORBIDDEN),  # сторонний пользователь в данном случае
            (self.moder_user, 'delete', status.HTTP_403_FORBIDDEN),  # модератор
            (self.user, 'delete', status.HTTP_204_NO_CONTENT),  # владелец в данном случае
        ]

        for user, action, expected_status in test_cases:
            self.client.force_authenticate(user=user)

            if action == 'retrieve':
                url = reverse('materials:course-detail', args=(self.course.pk,))
                response = self.client.get(url)
            elif action == 'create':
                url = reverse('materials:course-list')
                response = self.client.post(url, {'name': 'Updated'})
            elif action == 'update':
                url = reverse('materials:course-detail', args=(self.course.pk,))
                response = self.client.patch(url, {'name': 'Updated'})
            elif action == 'delete':
                url = reverse('materials:course-detail', args=(self.course.pk,))
                response = self.client.delete(url)

            self.assertEqual(
                response.status_code,
                expected_status,
                f"Failed for user={user}, action={action}, got {response.status_code} expected {expected_status}"
            )