from unittest.mock import patch

from django.core.management import call_command
from django.db import OperationalError
from django.test import TestCase


class ManagementCommandTest(TestCase):
    """
    Test all core management commands
    """
    def test_wait_for_db_ready(self):
        """
        Test wait_for_db command when db is available
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as mocked:
            mocked.return_value = True
            call_command('wait_for_db')
            self.assertEqual(mocked.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, time_sleep):
        """
        Test wait_for_db waiting for db
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as mocked:
            mocked.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(mocked.call_count, 6)

