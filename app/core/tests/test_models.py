from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    """
    Test models here
    """
    def test_create_user_with_email_successfully(self) -> None:
        """
        Test creating user with email
        :return: None
        """
        email = 'test@mail.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
