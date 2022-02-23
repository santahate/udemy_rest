from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicApiTests(TestCase):
    """
    Test publicly available endpoints
    """
    def setUp(self):
        """
        Set up test data
        """
        self.client = APIClient()

    def test_login_required(self):
        """
        Test login is required for listing ingredients
        """
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(TestCase):
    """
    Test logged in user's available endpoints
    """
    def setUp(self):
        """
        Set up test data
        """
        self.user = get_user_model().objects.create_user(
            'mail@mail.ua',
            'password432'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """
        Test retrieving ingredients
        """
        Ingredient.objects.create(user=self.user, name='Milk')
        Ingredient.objects.create(user=self.user, name='Egg')

        response = self.client.get(INGREDIENTS_URL)

        tags = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_see_own_ingredients(self):
        """
        Test user can see only own ingredients
        """
        user2 = get_user_model().objects.create_user(
            'other@mail.com',
            'other_password'
        )
        Ingredient.objects.create(user=user2, name='Salt')
        ingredient = Ingredient.objects.create(user=self.user, name='Cheese')

        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], ingredient.name)

    def test_create_ingredient_success(self):
        """
        Test create ingredient
        """
        payload = {'name': 'potato'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects \
            .filter(name=payload['name'], user=self.user).exists()
        self.assertIs(exists, True)

    def test_create_ingredient_invalid(self):
        """
        Test create ingredient with invalid payload
        """
        payload = {'name': ''}
        response = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
