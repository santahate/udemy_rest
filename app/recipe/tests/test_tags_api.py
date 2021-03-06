from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


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
        Test login is required for listing tags
        """
        response = self.client.get(TAGS_URL)

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
            'password444'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """
        Test retrieving tags
        """
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Meat')

        response = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_see_own_tags(self):
        """
        Test user can see only own tags
        """
        user2 = get_user_model().objects.create_user(
            'other@mail.com',
            'other_password'
        )
        Tag.objects.create(user=user2, name='Fruit')
        tag = Tag.objects.create(user=self.user, name='Dessert')

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_create_tag_success(self):
        """
        Test create Tag
        """
        payload = {'name': 'tag name'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects\
            .filter(name=payload['name'], user=self.user).exists()
        self.assertIs(exists, True)

    def test_create_tag_invalid(self):
        """
        Test create Tag with imvalid payload
        """
        payload = {'name': ''}
        response = self.client.post(TAGS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
