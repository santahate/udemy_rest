from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Tag, Ingredient, Recipe


def sample_user(email='mail@mail.com', password='password123'):
    """
    Create a sample user
    """
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """
    Test models here
    """
    def test_create_user_with_email_successfully(self):
        """
        Test creating user with email
        """
        email = 'test@mail.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test new user email is normalized (should be case-insensitive)
        """
        email = 'test@MYSITE.COM'
        user = get_user_model().objects.create_user(
            email=email,
            password='123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating user with empty email raises error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='123')
            get_user_model().objects.create_user(email=None, password='123')

    def test_create_new_superuser(self):
        """
        Test superuser is created
        """
        user = get_user_model().objects.create_superuser(
            email='test@MYSITE.COM',
            password='123',
        )
        self.assertIs(user.is_superuser, True)
        self.assertIs(user.is_staff, True)

    def test_tag_str(self):
        """
        Test Tag str representation
        """
        tag = Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
            """
            Test Ingredient str representation
            """
            ingredient = Ingredient.objects.create(
                user=sample_user(),
                name='Cucumber'
            )
            self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """
        Test Recepi str representation
        """
        recipe = Recipe.objects.create(
            user=sample_user(),
            title='Mushroom souce',
            time=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)
