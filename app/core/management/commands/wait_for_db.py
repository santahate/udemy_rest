from time import sleep

from django.core.management import BaseCommand
from django.db import connections, OperationalError


class Command(BaseCommand):
    """
    Wait for db available
    """
    def handle(self, *args, **options):
        """
        pass
        """
        self.stdout.write('Waiting for db...')
        db_connection = None
        while not db_connection:
            try:
                db_connection = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 sec..')
                sleep(1)
                continue
        self.stdout.write(self.style.SUCCESS('Connected'))
