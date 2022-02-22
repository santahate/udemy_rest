from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')


def create_user(**kwargs):
    """
    Create user

    :param kwargs: user params
    """
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """
    Test user API public endpoints
    """
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """
        Test user create with valid payload
        """
        payload = {
            'email': 'mail@mail.com',
            'password': 'password',
            'name': 'testing name',
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertEqual(user.check_password(payload['password']), True)
        self.assertNotIn('password', response.data)

    def test_user_exist(self):
        """
        Test creating user that already exist
        """
        payload = {
            'email': 'mail@mail.com',
            'password': 'password',
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test password longer 5 char
        """
        payload = {
            'email': 'mail@mail.com',
            'password': 'qwe',
            'name': 'testing name'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects\
            .filter(email=payload['email']).exists()
        self.assertIs(user_exist, False)
