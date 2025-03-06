from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Subscription, Course
from users.models import User


# Create your tests here.
class MaterialsTestCase(APITestCase):

    def setUp(self) -> None:
        """Создание тестового пользователя и тестового урока"""
        self.user = User.objects.create_user(username="test user", password="test pass")
        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test Description",
            owner=self.user
        )

    def test_create_lesson(self):
        """ Тестирование создания урока """

        data = {
            'name': 'Test',
            'description': 'Test',
        }

        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 2, 'name': 'Test', 'description': 'Test', 'preview_image': None, 'video_link': None, 'course': None,
             'owner': 1}
        )

    def test_list_lesson(self):
        """ Тестирование вывода списка уроков """

        # Создаем дополнительные уроки
        lesson_1 = Lesson.objects.create(
            name='Test Lesson 1',
            description='Description for Lesson 1',
            owner=self.user
        )

        lesson_2 = Lesson.objects.create(
            name='Test Lesson 2',
            description='Description for Lesson 2',
            owner=self.user
        )

        # Отправляем запрос на получение списка уроков
        response = self.client.get('/lesson/')

        # Проверяем, что статус ответа 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Извлекаем результаты из ответа с пагинацией
        response_data = response.json()['results']

        # Сортируем данные по ID
        response_data_sorted = sorted(response_data, key=lambda x: x['id'])

        # Ожидаемые данные для проверки
        expected_data = [
            {
                'id': lesson_1.id,  # ID первого созданного урока
                'name': 'Test Lesson 1',
                'description': 'Description for Lesson 1',
                'preview_image': None,
                'video_link': None,
                'course': None,
                'owner': self.user.id
            },
            {
                'id': lesson_2.id,  # ID второго созданного урока
                'name': 'Test Lesson 2',
                'description': 'Description for Lesson 2',
                'preview_image': None,
                'video_link': None,
                'course': None,
                'owner': self.user.id
            },
            {
                'id': self.lesson.id,  # ID урока, созданного в setUp
                'name': 'Test Lesson',
                'description': 'Test Description',
                'preview_image': None,
                'video_link': None,
                'course': None,
                'owner': self.user.id
            }
        ]

        # Сортируем ожидаемые данные по ID
        expected_data_sorted = sorted(expected_data, key=lambda x: x['id'])

        # Сравниваем отсортированные данные
        self.assertEqual(response_data_sorted, expected_data_sorted)

    def test_retrieve_lesson(self):
        """ Тестирование получения одного урока """
        response = self.client.get(f'/lesson/{self.lesson.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.lesson.id)

    def test_update_lesson(self):
        """ Тестирование обновления урока """
        data = {
            'name': 'Updated Lesson',
            'description': 'Updated Description'
        }

        response = self.client.put(f'/lesson/update/{self.lesson.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Updated Lesson')

    def test_destroy_lesson(self):
        """ Тестирование удаления урока """
        response = self.client.delete(f'/lesson/delete/{self.lesson.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_subscription(self):
        """ Тестирование подписки """

        # Создаем курс для подписки
        course = Course.objects.create(
            name='list test',
            description='list test',
            owner=self.user  # Добавляем владельца курса
        )

        # Отправляем запрос для подписки на курс
        data = {'course_id': course.id}  # Передаем ID курса
        response = self.client.post('/subscription/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Извлекаем сообщение из ответа
        response_data = response.json()
        self.assertIn('message', response_data)  # Проверяем, что в ответе есть сообщение

        # Проверяем, что подписка была добавлена
        subscription = Subscription.objects.filter(user=self.user, course=course).exists()
        self.assertTrue(subscription)

        # Проверяем, что сообщение соответствует ожидаемому
        self.assertEqual(response_data['message'], 'Подписка добавлена')
