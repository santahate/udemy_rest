from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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

    def test_create_token(self):
        """
        Test token is created
        """
        payload = {
            'email': 'mail@mail.com',
            'password': 'qwe',
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_token_invalid_credentials(self):
        """
        Test token is not created if invalid credentials passed
        """
        payload = {
            'email': 'mail@mail.com',
            'password': 'qwe',
        }
        create_user(**payload)
        payload['password'] = 'wrong_pass'
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_create_token_no_user(self):
        """
        Test token not created if user not exists
        """
        payload = {
            'email': 'mail@mail.com',
            'password': 'wrong_pass'
        }
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_create_token_missing_credential(self):
        """
        Test email and password are required
        """
        payload = {
            'email': 'mail@mail.com',
            'password': '',
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            'email': '',
            'password': 'password123',
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test auth is required for users
        """
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """
    Test user API endpoints that require auth
    """
    def setUp(self):
        self.user = create_user(
            email='email@mail.com',
            password='password321',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile(self):
        """
        Test retrieve profile for logged in user
        """
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """
        Test POST method is not allowed on ME_URL
        """
        response = self.client.post(ME_URL, {})

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_udpate_user_profile(self):
        """
        Test updating user profile
        """
        payload = {
            'name': 'new_name',
            'password': 'new_password'
        }

        response = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertIs(self.user.check_password(payload['password']), True)
