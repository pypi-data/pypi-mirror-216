from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class NoMissingMigrationsTest(TestCase):
    def test_no_missing_migrations(self):
        out = StringIO()
        call_command('makemigrations', dry_run=True, stdout=out)
        self.assertEqual(out.getvalue(), 'No changes detected\n')
