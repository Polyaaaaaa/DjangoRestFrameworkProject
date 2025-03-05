from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
class MaterialsTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_lesson(self):
        """ Тестирование создания урока"""
        data = {
            'name': 'Test',
            'description': 'Test',
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
