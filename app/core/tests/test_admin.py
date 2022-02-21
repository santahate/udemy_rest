from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    """
    All admin site tests
    """
    def setUp(self):
        """
        Run before every test
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='afmin@mail.com',
            password='ppp123'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='user@user.com',
            password='rrr333',
            name='Test user full name'
        )

    def test_users_listed(self):
        """
        Test users are listed on users admin page
        """
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """
        Test user edit page works
        """
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """
        Test create user page works
        """
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
