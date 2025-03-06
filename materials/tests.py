from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson
from users.models import User


# Create your tests here.
class MaterialsTestCase(APITestCase):

    def setUp(self) -> None:
        """Создание тестового пользователя"""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

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
            {'id': 1, 'name': 'Test', 'description': 'Test', 'preview_image': None, 'video_link': None, 'course': None,
             'owner': 1}
        )

    def test_list_lesson(self):
        """ Тестирование вывода списка уроков """

        Lesson.objects.create(
            name='list test',
            description='list test',
            owner=self.user  # Добавляем владельца урока
        )

        response = self.client.get('/lesson/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Извлекаем результаты из ответа с пагинацией
        response_data = response.json()['results']

        expected_data = [{
            'id': 2,
            'name': 'list test',
            'description': 'list test',
            'preview_image': None,
            'video_link': None,
            'course': None,
            'owner': self.user.id  # Используем ID тестового пользователя
        }]

        self.assertEqual(response_data, expected_data)

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

        response = self.client.put(f'/lesson/{self.lesson.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Updated Lesson')

    def test_destroy_lesson(self):
        """ Тестирование удаления урока """
        response = self.client.delete(f'/lesson/{self.lesson.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_subscription(self):
        """ Тестирование подписки """
        Lesson.objects.create(
            name='list test',
            description='list test',
            owner=self.user  # Добавляем владельца урока
        )
        response = self.client.get('/lesson/')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Извлекаем результаты из ответа с пагинацией
        response_data = response.json()['results']
        expected_data = [{
            'id': 2,
            'name': 'list test',
            'description': 'list test',
            'preview_image': None,
            'video_link': None,
            'course': None,
            'owner': self.user.id  # Используем ID тестового пользователя
        }]
        self.assertEqual(response_data, expected_data)
